#!/usr/bin/env python3
"""
ig_reel_downloader_poster.py

Standalone script: downloads Instagram Reels from configured source accounts
and reposts them with:
  - Original caption preserved (@mentions replaced with your POSTER_ACCOUNT)
  - Hashtags from original post; if none, placeholder hashtags appended
  - POSTER_ACCOUNT watermark burned into the video (bottom-right)

Usage:
    python ig_reel_downloader_poster.py

Prerequisites:
    - Run src/start.py first to configure USERNAME, PASSWORD, ACCOUNTS,
      POSTER_ACCOUNT, and HASTAGS — or set them directly in src/config.py
"""

import sys
import os

# Must happen before any src/ imports — config.py computes DB/download paths
# using os.getcwd(), and auth.py looks for session.json relative to cwd.
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
os.chdir(SRC_DIR)
sys.path.insert(0, SRC_DIR)

import re
import json
import logging
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

from rich import print as rprint
from rich.rule import Rule

import config
import auth
import helpers as Helper
from db import Session, Reel, ReelEncoder
from captions_db import save_caption, get_processed_caption

# Suppress moviepy progress bars
import moviepy.config as mpy_conf
try:
    mpy_conf.FFMPEG_BINARY  # noqa: just importing to suppress
except Exception:
    pass
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

logging.basicConfig(
    filename='application.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def _poster_account():
    """Return the configured poster account name (without @), falling back to USERNAME."""
    account = getattr(config, 'POSTER_ACCOUNT', '') or ''
    if not account.strip() or account == 'your_username':
        account = getattr(config, 'USERNAME', '') or ''
    return account.strip().lstrip('@')


# ------------------------------------------------------------------ #
# Caption processing
# ------------------------------------------------------------------ #

def process_caption(original):
    """Return a ready-to-post caption from the scraped original.

    - All @mentions → @<POSTER_ACCOUNT>
    - Hashtags from original kept; if none, configured placeholders appended
    """
    text = original or ''
    text = re.sub(r'@\w+', f'@{_poster_account()}', text)

    if not re.search(r'#\w+', text):
        try:
            placeholder = Helper.get_config('HASTAGS')
            if not placeholder:
                raise ValueError
        except Exception:
            placeholder = config.HASHTAGS
        if placeholder and placeholder.strip():
            text = text.rstrip() + ('\n\n' if text.strip() else '') + placeholder.strip()

    return text.strip()


# ------------------------------------------------------------------ #
# Watermark
# ------------------------------------------------------------------ #

def add_watermark(input_path):
    """Burn the configured POSTER_ACCOUNT as a text watermark into the video. Returns watermarked file path."""
    out_path = input_path.rsplit('.', 1)[0] + '_wm.mp4'
    if os.path.exists(out_path):
        return out_path

    clip = VideoFileClip(input_path)
    try:
        txt = (
            TextClip(
                f'@{_poster_account()}',
                fontsize=36,
                color='white',
                stroke_color='black',
                stroke_width=1.5,
                font='Arial',
            )
            .set_position(lambda t: ('right', 'bottom'))
            .margin(right=15, bottom=15, opacity=0)
            .set_duration(clip.duration)
        )
        final = CompositeVideoClip([clip, txt])
        final.write_videofile(
            out_path,
            codec='libx264',
            audio_codec='aac',
            logger=None,
            verbose=False,
        )
    finally:
        clip.close()

    return out_path


# ------------------------------------------------------------------ #
# Download phase
# ------------------------------------------------------------------ #

def download_reels(api):
    """Fetch reels from all configured ACCOUNTS, download new ones.

    Returns count of newly downloaded reels.
    """
    Helper.load_all_config()
    session = Session()
    downloaded = 0

    for account in config.ACCOUNTS:
        rprint(f'[bold cyan]Scraping account:[/bold cyan] @{account}')
        try:
            user_id = api.user_id_from_username(account)
            medias = api.user_medias(user_id, int(config.FETCH_LIMIT))
            # Fixed filter (original reels.py had a tuple-condition bug)
            reels = [m for m in medias if m.product_type == 'clips' or m.media_type == 2]
            rprint(f'  Found {len(reels)} reel(s)')

            for reel in reels:
                if not reel.video_url:
                    continue
                try:
                    exists = session.query(Reel).filter_by(code=reel.code).first()
                    if exists:
                        continue

                    filename = reel.video_url.split('/')[-1].split('?')[0]
                    filepath = config.DOWNLOAD_DIR + filename

                    rprint(f'  [cyan]Downloading[/cyan] {reel.code} ...')
                    dl_path = api.video_download_by_url(reel.video_url, folder=config.DOWNLOAD_DIR)
                    # Use the path returned by instagrapi (may differ from constructed path)
                    actual_path = str(dl_path) if dl_path else filepath

                    processed = process_caption(reel.caption_text)

                    reel_db = Reel(
                        post_id=str(reel.id),
                        code=reel.code,
                        account=account,
                        caption=reel.caption_text,
                        file_name=filename,
                        file_path=actual_path,
                        is_posted=False,
                        data=_safe_encode(reel),
                    )
                    session.add(reel_db)
                    session.commit()

                    save_caption(reel.code, reel.caption_text or '', processed)

                    downloaded += 1
                    rprint(f'  [green]Saved[/green] {reel.code}')

                except Exception as e:
                    rprint(f'  [red]Error downloading {reel.code}: {e}[/red]')
                    logging.exception('Download error for %s', reel.code)
                    session.rollback()

        except Exception as e:
            rprint(f'  [red]Could not fetch @{account}: {e}[/red]')
            logging.exception('Account fetch error: %s', account)

    session.close()
    return downloaded


def _safe_encode(reel):
    try:
        return json.dumps(reel, cls=ReelEncoder)
    except Exception:
        return '{}'


# ------------------------------------------------------------------ #
# Post phase
# ------------------------------------------------------------------ #

def post_reels(api):
    """Post all unposted reels with watermark and processed caption.

    Returns count of successfully posted reels.
    """
    Helper.load_all_config()

    fetch_session = Session()
    unposted = fetch_session.query(Reel).filter_by(is_posted=False).all()
    fetch_session.close()

    if not unposted:
        rprint('[yellow]No unposted reels found.[/yellow]')
        return 0

    rprint(f'[bold]Posting {len(unposted)} reel(s)...[/bold]')
    posted = 0

    for reel in unposted:
        if not os.path.exists(reel.file_path):
            rprint(f'  [yellow]File missing, skipping:[/yellow] {reel.file_path}')
            continue

        caption = get_processed_caption(reel.code) or process_caption(reel.caption)

        try:
            rprint(f'  [cyan]Watermarking[/cyan] {reel.code} ...')
            wm_path = add_watermark(reel.file_path)
        except Exception as e:
            rprint(f'  [yellow]Watermark failed, using original: {e}[/yellow]')
            logging.warning('Watermark failed for %s: %s', reel.code, e)
            wm_path = reel.file_path

        try:
            rprint(f'  [cyan]Uploading[/cyan] {reel.code} ...')
            api.delay_range = [1, 3]
            media = api.clip_upload(
                wm_path,
                caption,
                extra_data={
                    'like_and_view_counts_disabled': int(config.LIKE_AND_VIEW_COUNTS_DISABLED),
                    'disable_comments': int(config.DISABLE_COMMENTS),
                },
            )

            if media:
                update_session = Session()
                update_session.query(Reel).filter_by(code=reel.code).update(
                    {'is_posted': True, 'posted_at': datetime.now()}
                )
                update_session.commit()
                update_session.close()
                posted += 1
                rprint(f'  [green]Posted[/green] {reel.code}')

        except Exception as e:
            rprint(f'  [red]Upload failed for {reel.code}: {e}[/red]')
            logging.exception('Post error for %s', reel.code)

    return posted


# ------------------------------------------------------------------ #
# Entry point
# ------------------------------------------------------------------ #

def main():
    Helper.load_all_config()
    rprint(Rule('[bold blue]Instagram Reels Downloader & Poster[/bold blue]'))
    rprint(f'Poster account: [bold magenta]@{_poster_account()}[/bold magenta]')

    try:
        api = auth.login()
    except Exception as e:
        rprint(f'[bold red]Login failed: {e}[/bold red]')
        sys.exit(1)

    rprint(Rule('[bold]Phase 1 — Downloading Reels[/bold]'))
    downloaded = download_reels(api)
    rprint(f'[green]Downloaded {downloaded} new reel(s).[/green]')

    rprint(Rule('[bold]Phase 2 — Posting Reels[/bold]'))
    posted = post_reels(api)
    rprint(f'[green]Posted {posted} reel(s).[/green]')

    rprint(Rule('[bold green]Done[/bold green]'))


if __name__ == '__main__':
    main()

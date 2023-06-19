import sys
import os
import re
import requests
from googleapiclient.discovery import build
import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor
import config
import json
import time
from db import Session, Reel
import helpers as Helper
from helpers import print


# Logger class to handle yt_dlp log messages
class Logger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

# Function to download shorts video using yt-dlp
def download_shorts_video(video_url: str, output_directory: str = "downloads") -> str:
    ydl_opts = {
        "outtmpl": os.path.join(output_directory, "%(title)s-%(id)s.%(ext)s"),
        "format": "best[height<=1080]",
        "logger": Logger(),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_default_info_extractors()
        info_dict = ydl.extract_info(video_url, download=False)
        output_filename = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
        return output_filename

# Function to extract channel ID from the given channel link
def extract_channel_id(channel_link: str) -> str:
    pattern = r"(?:youtube\.com/channel/)([^/?&]+)"
    match = re.search(pattern, channel_link)
    if match:
        return match.group(1)
    else:
        response = requests.get(channel_link)
        if response.status_code == 200:
            pattern = r'<meta itemprop="channelId" content="([^"]+)">'
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
            else:
                raise ValueError("Unable to extract channel ID from channel link")
        else:
            raise ValueError("Unable to fetch channel link")

# Function to get shorts videos from a YouTube channel using YouTube API
def get_shorts_videos(channel_id: str, api_key: str, max_results: int = 50):
    youtube = build("youtube", "v3", developerKey=api_key)

    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    shorts_videos = []
    next_page_token = None

    while True:
        playlist_items_request = youtube.playlistItems().list(
            part="snippet",
            maxResults=max_results,
            playlistId=uploads_playlist_id,
            pageToken=next_page_token
        )

        playlist_items = playlist_items_request.execute()

        for item in playlist_items["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            video_description = item["snippet"]["description"]

            if "#shorts" in video_title.lower() or "#shorts" in video_description.lower():
                shorts_videos.append({
                    "id": video_id,
                    "title": video_title,
                    "description": video_description,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })

        next_page_token = playlist_items.get("nextPageToken")
        if not next_page_token:
            break

    return shorts_videos

# Main function to process each channel and download shorts videos
def main():
    Helper.load_all_config()
    api_key = config.YOUTUBE_API_KEY
    output_directory = config.DOWNLOAD_DIR
    session = Session()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for channel_link in config.CHANNEL_LINKS:
        channel_id = extract_channel_id(channel_link)
        print(f"Channel ID: {channel_id}")
        shorts = get_shorts_videos(channel_id, api_key)

        for short_video in shorts:
            print(f"Downloading {short_video['title']} ({short_video['url']})")
            exists = session.query(Reel).filter_by(code=short_video['id']).first()
            if not exists:
                downloaded_file = download_shorts_video(short_video["url"], output_directory)
                print(f"Downloaded to: {downloaded_file}")
                reel_db = Reel(
                    post_id=short_video['id'],
                    code=short_video['id'],
                    account=channel_id,
                    caption=short_video['title'],
                    file_name=os.path.basename(downloaded_file),
                    file_path=downloaded_file,
                    data=json.dumps(short_video),
                    is_posted=False,
                    # posted_at = NULL
                )
                session.add(reel_db)
                session.commit()
                
    session.close()

    # Interval
#     time.sleep(int(config.YOUTUBE_SCRAPING_INTERVAL_IN_MINS) * 60)

# if __name__ == "__main__":
#     main()
   
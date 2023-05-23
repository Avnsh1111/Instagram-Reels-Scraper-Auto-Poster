import os
from instagrapi import Client
from src.db import Session, Reel, ReelEncoder
from datetime import datetime
import config
import time

# Update is_posted and posted_at field in DB
def update_status(code):
    session = Session()
    session.query(Reel).filter_by(code=code).update({'is_posted': True, 'posted_at': datetime.now()})
    session.commit()
    session.close()


# Get Unposted reels from database
def get_reel():
    session = Session()
    reel = session.query(Reel).filter_by(is_posted=False).first()
    session.close()
    return reel


# Magic Starts Here
def main(api):
    try:
        reel = get_reel()
        if os.path.exists(reel.file_path):
            media = api.clip_upload(
                reel.file_path,
                "Repost From Author : @" + reel.account + " , Caption : " + reel.caption + " " + config.HASHTAGS,
                extra_data={
                    # "custom_accessibility_caption": "alt text example",
                    "like_and_view_counts_disabled": config.LIKE_AND_VIEW_COUNTS_DISABLED,
                    "disable_comments": config.DISABLE_COMMENTS,
                })

            if media:
                update_status(reel.code)
            pass

    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        exit()
        pass
import os
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
from db import Session, Reel, ReelEncoder
from datetime import datetime
import config
import auth
import time
import helpers as Helper
from moviepy.editor import VideoFileClip
import logging
logging.getLogger("moviepy").setLevel(logging.ERROR)

from helpers import print

# Trim Video for story
def trim_video(file_path, output_path, max_duration=15):
    clip = VideoFileClip(file_path)
    trimmed_clip = clip.subclip(0, max_duration)
    trimmed_clip.write_videofile(output_path)
    return output_path

# Get Video Duration
def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    return duration

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
    print(reel.file_path)
    session.close()
    return reel

def post_to_story(api,media,media_path):

    username = api.user_info_by_username(config.USERNAME)
    hashtag = api.hashtag_info('like')

    duration = get_video_duration(media_path)
    if duration > 15:
        media_path = trim_video(media_path,config.DOWNLOAD_DIR+os.sep+media.code+".mp4")

    media_pk = api.media_pk_from_url('https://www.instagram.com/p/'+media.code+'/')

    api.video_upload_to_story(
        media_path,
        "",
        mentions=[StoryMention(user=username, x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
        links=[StoryLink(webUri='https://www.instagram.com/p/'+media.code+'/')],
        hashtags=[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)],
        medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
    )

# Magic Starts Here
def main(api):
    Helper.load_all_config()
    try:
        reel = get_reel()
        if os.path.exists(reel.file_path):
            api.delay_range = [1, 3]
            media = api.clip_upload(
                reel.file_path,
                config.HASHTAGS, #Caption
                extra_data={
                    # "custom_accessibility_caption": "alt text example",
                    "like_and_view_counts_disabled": config.LIKE_AND_VIEW_COUNTS_DISABLED,
                    "disable_comments": config.DISABLE_COMMENTS,
                })

            if media:
                update_status(reel.code)
                if int(config.IS_POST_TO_STORY) == 1 :
                    post_to_story(api,media,reel.file_path)                
                
        pass

    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        pass

# if __name__ == "__main__":
#     api = auth.login()
#     main(api)
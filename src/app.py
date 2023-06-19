import time
import config
import helpers as Helper
import reels,poster,shorts,remover
from instagrapi import Client
import auth
from datetime import datetime, timedelta

Helper.load_all_config()

next_reels_scraper_run_at = datetime.now()
next_poster_run_at = datetime.now()
next_remover_run_at = datetime.now()
next_youtube_run_at = datetime.now()

if config.IS_ENABLED_REELS_SCRAPER == "1" or config.IS_ENABLED_AUTO_POSTER == "1" : 
        #Instagram login client is here
        api = auth.login()

while True:
    
    if config.IS_ENABLED_REELS_SCRAPER == "1" or config.IS_ENABLED_AUTO_POSTER == "1" :     

        if config.IS_ENABLED_REELS_SCRAPER == "1" :
            if next_reels_scraper_run_at < datetime.now() :
                reels.main(api)
                next_reels_scraper_run_at =  datetime.now() + timedelta(seconds=int(config.SCRAPER_INTERVAL_IN_MIN)*60)

        if config.IS_ENABLED_AUTO_POSTER == "1" :
            if next_poster_run_at < datetime.now() :
                poster.main(api)
                next_poster_run_at =  datetime.now() + timedelta(seconds=int(config.POSTING_INTERVAL_IN_MIN)*60)

    
        
    if config.IS_REMOVE_FILES == "1" :
        if next_remover_run_at < datetime.now() :
            remover.main()
            next_remover_run_at =  datetime.now() + timedelta(seconds=int(config.REMOVE_FILE_AFTER_MINS)*60)

    if config.IS_ENABLED_YOUTUBE_SCRAPING == "1":
        if next_youtube_run_at < datetime.now() :
            shorts.main()
            next_youtube_run_at =  datetime.now() + timedelta(seconds=int(config.SCRAPER_INTERVAL_IN_MIN)*60)

    time.sleep(1)
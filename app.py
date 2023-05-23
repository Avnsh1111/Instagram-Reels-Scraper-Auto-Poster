import threading
import time
import config
from src import reels,poster,shorts,remover
from instagrapi import Client

# Set interval for Reels Scraper
def set_interval_for_reels(func, interval):
    while True:
        func(api)
        time.sleep(interval)

# Set interval for Auto Poster
def set_interval_for_poster(func, interval):
    while True:
        func(api)
        time.sleep(interval)

# Set interval for Youtube Scraper
def set_interval_for_shorts(func, interval):
    while True:
        func()
        time.sleep(interval)

# Set interval for Youtube Scraper
def set_interval_for_remover(func, interval):
    while True:
        func()
        time.sleep(interval)


#Creating Insta client
if config.IS_ENABLED_REELS_SCRAPER == 1 or config.IS_ENABLED_AUTO_POSTER == 1 : 
    #Instagram login client is here
    api = Client()
    try : 
        api.login(config.USERNAME, config.PASSWORD)
        pass
    except Exception as e:
        print(f"Exception {type(e).__name__}: {str(e)}")
        exit()


# Start the threads

# Reels Thread
if config.IS_ENABLED_REELS_SCRAPER == 1 :
    reelsScraperThread = threading.Thread(target=set_interval_for_reels, args=(reels.main, config.SCRAPER_INTERVAL_IN_MIN*60))
    reelsScraperThread.start()

# Poster Thread
if config.IS_ENABLED_AUTO_POSTER == 1 :
    posterThread = threading.Thread(target=set_interval_for_poster, args=(poster.main, config.POSTING_INTERVAL_IN_MIN*60))
    posterThread.start()

# Shorts Thread
if config.IS_ENABLED_YOUTUBE_SCRAPING == 1 :
    shortsThread = threading.Thread(target=set_interval_for_shorts, args=(shorts.main, config.SCRAPER_INTERVAL_IN_MIN*60))
    shortsThread.start()

# Remover Thread
if config.IS_REMOVE_FILES == 1 :
    removerThread = threading.Thread(target=set_interval_for_remover, args=(remover.main, config.REMOVE_FILE_AFTER_MINS*10))
    removerThread.start()

#End of Threads
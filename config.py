import os

#Config Variables
CURRENT_DIR = os.getcwd() + os.sep

#SQLite DB path
DB_PATH = CURRENT_DIR + 'database' + os.sep + 'sqlite.db'

#Download Path
DOWNLOAD_DIR = CURRENT_DIR + 'downloads' + os.sep #Path of folder where files will be stored

# Fetch LIMIT for scraper script
FETCH_LIMIT = 10

# Posting interval in Minutes
POSTING_INTERVAL_IN_MIN = 15 # Every 15 Minutes

# Scraper interval in Minutes
SCRAPER_INTERVAL_IN_MIN = 720 # Every 12 hours

# Instagram Username & Password
USERNAME = "your_username"
PASSWORD = "your_password"

#YOUTUBE API KEY
YOUTUBE_API_KEY = "YOUR_API_KEY"

# Account List for scraping
ACCOUNTS = [
    "totalgaming_official",
    "carryminati",
    "techno_gamerz",
    "payalgamingg",
    "dynamo__gaming"
]

# YouTube Channel List short for scraping
CHANNEL_LINKS = [
    "https://www.youtube.com/@exampleChannleName."
]

# HASHTAGS to add while Posting
HASHTAGS = "#reels #shorts #likes #follow"

![Cover Image](images/cover.png)

# Reels-AutoPilot

Reels-AutoPilot is a powerful GitHub repository that scrapes reels from specified Instagram accounts and shorts from YouTube channels, and automatically posts them to your Instagram account. Keep up with the latest content from your favorite creators and effortlessly share it with your followers. Enhance your Instagram presence and grow your account with Reels-AutoPilot!

## Getting Started

Before using Reels-AutoPilot, set your configuration variables in the `config.py` file.

### Prerequisites

- Python 3.x
- A valid Instagram account
- A Google Developers Console project with the YouTube Data API enabled and an API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/avnsh1111/Instagram-Reels-Scraper-Auto-Poster.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Generate a YouTube API Key

1. Set up a Google Developers Console project and enable the YouTube Data API:

   a. Go to the [Google Developers Console](https://console.developers.google.com/).
   
   b. Create a new project by clicking the project drop-down menu, then click "New Project" and fill in the required fields, or select an existing project from the list.
   
   c. In the Dashboard, click on "Enable APIs and Services" and search for the "YouTube Data API v3". Click on it and then click the "Enable" button.
   
   d. Create an API key by going to "Credentials" in the left-hand menu, then click on "Create credentials" > "API key".

2. Once you have your API key, open the `config.py` file in the Reels-AutoPilot project and replace `YOUR_API_KEY` with your newly generated API key:

```python
YOUTUBE_API_KEY = "YOUR_API_KEY"
```

### Configuration

In `config.py`, set the following variables:

- `USERNAME`: Your Instagram username
- `PASSWORD`: Your Instagram password
- `ACCOUNTS`: An array of Instagram accounts to scrape reels from
- `CHANNEL_LINKS`: An array of YouTube channel links to scrape shorts from
- `YOUTUBE_API_KEY`: Your YouTube API key
- `FETCH_LIMIT`: Number of reels/shorts to fetch per account/channel
- `HASHTAGS`: Hashtags to add while reposting reels
- `POSTING_INTERVAL_IN_MIN`: Interval in minutes between reel/short postings
- `SCRAPER_INTERVAL_IN_MIN`: Interval in minutes between scraper runs

Example:

```python
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
HASHTAGS = "#gaming #gamer #ps #playstation #videogames #game #xbox #games #twitch #fortnite #pc #memes #pcgaming #gamers #gamingcommunity #youtube #xboxone #gamergirl #nintendo #gta #callofduty #streamer #follow #pubg #videogame #esports #bhfyp #meme #twitchstreamer #art"
```

## Usage

### Scraping Reels

To scrape reels from the specified accounts in `config.py`, run:

```bash
python reels.py
```

This will scrape reels and store them in the `downloads` folder.

### Scraping YouTube Shorts

To scrape shorts from the specified YouTube channels in `config.py`, run:

```bash
python shorts.py
```

This will scrape shorts and store them in the `downloads` folder.

### Posting Reels and Shorts

To post scraped reels and shorts to your Instagram account, run:

```bash
python poster.py
```

This will post reels and shorts at the specified interval in `config.py`.

## Contributing

To contribute to this project, submit pull requests or open issues with your suggestions and ideas.

## License

Reels-AutoPilot is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all developers who contributed to the libraries used in this project.

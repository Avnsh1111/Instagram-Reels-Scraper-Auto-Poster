![Cover Image](images/cover.png)

# Reels-AutoPilot

Reels-AutoPilot is a powerful GitHub repository that scrapes reels from specified Instagram accounts and shorts from YouTube channels, and automatically posts them to your Instagram account. Keep up with the latest content from your favorite creators and effortlessly share it with your followers. Enhance your Instagram presence and grow your account with Reels-AutoPilot!

# Active Sponsors
![coding-sunshine](https://avatars.githubusercontent.com/u/3206025?s=80&v=4)

### Looking For Sponsors
<a href="https://www.buymeacoffee.com/avnsh1111" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
&nbsp;&nbsp;
<noscript><a href="https://liberapay.com/avnsh1111/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>


## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Generate a YouTube API Key](#generate-a-youtube-api-key)
    - [Configuration](#configuration)
- [Usage](#usage)
- [Docker Configuration](#docker-configuration)
    - [Build the Docker Image](#build-the-docker-image)
    - [Run the Docker Container](#run-the-docker-container)
    - [Check Running Containers](#check-running-containers)
    - [Stop the Docker Container](#stop-the-docker-container)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Additional Features](#additional-features)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Troubleshooting](#troubleshooting)
- [Changelog](#changelog)

## Getting Started

Before using Reels-AutoPilot, set your configuration variables in the `config.py` file.

### Prerequisites

- Python 3.x
- A valid Instagram account
- A Google Developers Console project with the YouTube Data API enabled and an API key
- Docker (optional)

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
## Remover Configurations
- `IS_REMOVE_FILES`: 0 = Keep Files; 1 = Delete Posted Files;
- `REMOVE_FILE_AFTER_MINS`: Interval in minutes to remover files
## Instagram Configurations
- `IS_ENABLED_REELS_SCRAPER`: 0/1 = Turn Off/Turn On Reels Scraper
- `IS_ENABLED_AUTO_POSTER`: 0/1 = Turn Off/Turn On Auto Poster
- `FETCH_LIMIT`: Number of reels/shorts to fetch per account/channel
- `POSTING_INTERVAL_IN_MIN`: Interval in minutes between reel/short postings
- `USERNAME`: Your Instagram username
- `PASSWORD`: Your Instagram password
- `ACCOUNTS`: An array of Instagram accounts to scrape reels from
- `SCRAPER_INTERVAL_IN_MIN`: Interval in minutes between scraper runs
- `LIKE_AND_VIEW_COUNTS_DISABLED`: 0/1 = Disable/Enable Like and View 
- `DISABLE_COMMENTS`: 0/1 = Disbale/Enable comments
- `HASHTAGS`: Hashtags to add while reposting reels
## Youtube Configurations
- `IS_ENABLED_YOUTUBE_SCRAPING`: 0/1 = Turn Off/Turn On Shorts Scraper
- `YOUTUBE_API_KEY`: Your YouTube API key
- `CHANNEL_LINKS`: An array of YouTube channel links to scrape shorts from





Example:

```python
import os

#-------------------------------
# Global Configurations
#-------------------------------

# Config Variables
CURRENT_DIR = os.getcwd() + os.sep

# SQLite DB path
DB_PATH = CURRENT_DIR + 'database' + os.sep + 'sqlite.db'

# Download Path
DOWNLOAD_DIR = CURRENT_DIR + 'downloads' + os.sep  # Path of folder where files will be stored

#IS REMOVE FILES
IS_REMOVE_FILES = 1

# Remove Posted Files Interval
REMOVE_FILE_AFTER_MINS = 120 #every two hours

#-------------------------------
# Instagram Configurations
#-------------------------------

# IS RUN REELS SCRAPER
IS_ENABLED_REELS_SCRAPER = 1

# IS RUN AUTO POSTER
IS_ENABLED_AUTO_POSTER = 1

# Fetch LIMIT for scraper script
FETCH_LIMIT = 10

# Posting interval in Minutes
POSTING_INTERVAL_IN_MIN = 15  # Every 15 Minutes

# Scraper interval in Minutes
SCRAPER_INTERVAL_IN_MIN = 720  # Every 12 hours

# Instagram Username & Password
USERNAME = "your_username"
PASSWORD = "your_password"

# Account List for scraping
ACCOUNTS = [
    "totalgaming_official",
    "carryminati",
    "techno_gamerz",
    "payalgamingg",
    "dynamo__gaming"
]

# like_and_view_counts_disabled
LIKE_AND_VIEW_COUNTS_DISABLED = 0

# disable_comments
DISABLE_COMMENTS = 0

# HASHTAGS to add while Posting
HASHTAGS = "#reels #shorts #likes #follow"

#-------------------------------
# Youtube Configurations
#-------------------------------

# IS RUN YOUTUBE SCRAPER
IS_ENABLED_YOUTUBE_SCRAPING = 0

# YOUTUBE API KEY
YOUTUBE_API_KEY = "YOUR_API_KEY"

# YouTube Channel List short for scraping
CHANNEL_LINKS = [
    "https://www.youtube.com/@exampleChannleName."
]
```

## Usage

Based on `config.py` this script will run all commands

-  Example: `IS_ENABLED_REELS_SCRAPER = 1` then `app.py` itself run the reels scraper as so on for Auto poster : `IS_ENABLED_AUTO_POSTER=1` and for shorts scraper : `IS_ENABLED_YOUTUBE_SCRAPING = 1`

```bash
python app.py
```

This will post reels and shorts at the specified interval in `config.py`.

## Docker Configuration

You can also use Docker to build and run Reels-AutoPilot.

### Build the Docker Image

To build the Docker image, run:

```bash
docker-compose build
```

### Run the Docker Container

To run the Docker container, run:

```bash
docker-compose up -d
```

### Check Running Containers

To check the running Docker containers, run:

```bash
docker-compose ps
```

### Stop the Docker Container

To stop the Docker container, run:

```bash
docker-compose down
```

## Contributing

To contribute to this project, submit pull requests or open issues with your suggestions and ideas.

## License

Reels-AutoPilot is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all developers who contributed to the libraries used in this project.

## Frequently Asked Questions

#### Q: Can I run Reels-AutoPilot on a Raspberry Pi or similar devices?

A: Yes, Reels-AutoPilot can be run on a Raspberry Pi or any other device that supports Python 3.x and the required dependencies. However, you may need to adjust the configuration and installation steps to match the specific requirements of your device.

#### Q: Can I use Reels-AutoPilot for commercial purposes?

A: Reels-AutoPilot is released under the GNU General Public License v3.0, which allows you to use, modify, and distribute the software for both personal and commercial purposes. However, you must comply with the terms of the license, which includes providing the source code for any modifications you make and preserving the original copyright notices.

#### Q: Is it safe to use my Instagram account credentials with Reels-AutoPilot?

A: Reels-AutoPilot stores your Instagram account credentials in the `config.py` file, and they are used only for authenticating and posting reels andshorts to your account. However, make sure to keep your credentials secure and not share them with unauthorized parties. It is also recommended to use a secondary Instagram account for testing purposes before using your main account.

#### Q: Can I post reels and shorts from private Instagram accounts or YouTube channels?

A: Reels-AutoPilot can only scrape reels from public Instagram accounts and shorts from public YouTube channels. If you want to post content from private accounts or channels, you will need to obtain the necessary permissions and access to the content.

#### Q: Can I get banned from Instagram for using Reels-AutoPilot?

A: Reels-AutoPilot automates the process of posting reels and shorts to your Instagram account. While automation can potentially violate Instagram's terms of service, Reels-AutoPilot is designed to minimize the risk of getting banned by posting at regular intervals and not spamming your account. However, it is still recommended to use Reels-AutoPilot responsibly and at your own risk.

## Troubleshooting

1. **Issue**: Reels-AutoPilot is not scraping reels or shorts correctly.

   **Solution**: Ensure that the Instagram account usernames and YouTube channel links in `config.py` are correct and publicly accessible. Also, make sure that your YouTube API key is valid and has not exceeded the quota limits.

2. **Issue**: Reels-AutoPilot is not posting reels and shorts to my Instagram account.

   **Solution**: Verify that your Instagram account credentials in `config.py` are correct and that your account has not been banned or restricted. Additionally, check the `POSTING_INTERVAL_IN_MIN` and `SCRAPER_INTERVAL_IN_MIN` settings to ensure they are set to appropriate values.

3. **Issue**: I am receiving an error when running Reels-AutoPilot with Docker.

   **Solution**: Make sure you have properly installed and configured Docker on your system. Double-check the Docker build and run commands to ensure they are executed correctly. If the issue persists, consider running Reels-AutoPilot without Docker.

If you continue to face issues or need further assistance, please open an issue on the GitHub repository or reach out to the community for support.

## Changelog

- **v1.0.0** - Initial release with basic scraping and posting features.
- **v1.1.0** - Added support for scraping YouTube shorts and improved error handling.
- **v1.2.0** - Implemented Docker configuration and enhanced documentation.
- **v1.3.0** - Implemented Remover and process threading also resolved docker issue.

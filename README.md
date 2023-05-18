![Cover Image](images/cover.png)

# Reels-AutoPilot

Reels-AutoPilot is a powerful GitHub repository that scrapes reels from specified Instagram accounts and shorts from YouTube channels, and automatically posts them to your Instagram account. Keep up with the latest content from your favorite creators and effortlessly share it with your followers. Enhance your Instagram presence and grow your account with Reels-AutoPilot!

### Looking For Sponsors

<noscript><a href="https://liberapay.com/avnsh1111/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>


## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Generate a YouTube API Key](#generate-a-youtube-api-key)
    - [Configuration](#configuration)
- [Usage](#usage)
    - [Scraping Reels](#scraping-reels)
    - [Scraping YouTube Shorts](#scraping-youtube-shorts)
    - [Posting Reels and Shorts](#posting-reels-and-shorts)
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

## Docker Configuration

You can also use Docker to build and run Reels-AutoPilot.

### Build the Docker Image

To build the Docker image, run:

```bash
docker build -t reels-autopilot .
```

### Run the Docker Container

To run the Docker container, run:

```bash
docker run -d reels-autopilot
```

### Check Running Containers

To check the running Docker containers, run:

```bash
docker ps
```

### Stop the Docker Container

To stop the Docker container, run:

```bash
docker stop <container_id>
```

## Contributing

To contribute to this project, submit pull requests or open issues with your suggestions and ideas.

## License

Reels-AutoPilot is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all developers who contributed to the libraries used in this project.

## Additional Features

1. Reels and shorts scheduling: Schedule specific reels and shorts to be posted at certain times or dates.
2. Custom captions: Add custom captions to each reel or short when posting.
3. Multiple Instagram accounts: Support for posting reels and shorts to multiple Instagram accounts.
4. Auto-hashtag generation: Automatically generate relevant hashtags based on the content of a reel or short.
5. Analytics and insights: Collect data on the performance of your posted reels and shorts, such as views, likes, and comments.

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

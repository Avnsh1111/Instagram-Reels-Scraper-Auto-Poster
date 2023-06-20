# DB
from db import Session, Reel, Config
from sqlalchemy import desc

# Date Time
from datetime import datetime

# Rich
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box
from rich.console import Console, Group

# Reels-AutoPilot Config
import config
import logging

logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def print(message) :
    logging.info(message)

# Get Config
def get_config(key_name) :
    session = Session()
    reel = session.query(Config).filter_by(key=key_name).first()
    session.close()
    return reel.value

# Get the configuration data from the database
def get_all_config():
    session = Session()
    config_values = session.query(Config).all()
    session.close()
    return config_values;

# Load all Config
def load_all_config() : 
     for config_val in get_all_config():
        
        if config_val.key == "ACCOUNTS" or config_val.key == "CHANNEL_LINKS" :
            setattr(config, config_val.key, config_val.value.split(","))
        else:
            setattr(config, config_val.key, config_val.value)

# Save config by key Value
def save_config(key,value) :
    session = Session()
    exists = session.query(Config).filter_by(key=key).first()
    if not exists:
        config_db = Config(
                    key=key,
                    value=value,
                    created_at = datetime.now(),
                    updated_at = datetime.now(),
                    )
        session.add(config_db)
        session.commit()
    else:
        session.query(Config).filter_by(key=key).update({'value': value, 'updated_at': datetime.now()})

         
    session.close()

# Display the information about the developer
def make_my_information() -> Panel:
    sponsor_message = Table.grid(padding=0)
    sponsor_message.add_column(style="green", justify="center")
    sponsor_message.add_row("[red]▄▀█ █░█ █ █▄░█ ▄▀█ █▀ █░█   █▀█ ▄▀█ ▀█▀ █░█ █▀█ █▀▄[/red]")
    sponsor_message.add_row("[red]█▀█ ▀▄▀ █ █░▀█ █▀█ ▄█ █▀█   █▀▄ █▀█ ░█░ █▀█ █▄█ █▄▀[/red]")
    
    sponsor_message.add_row("")
    sponsor_message.add_row("I'm a highly motivated and dedicated developer, open-source contributor, and a never-ending learner with a strong passion for cutting-edge technologies and innovative solutions. I thoroughly enjoy collaborating with others to create outstanding products and contribute to the tech community.")
    sponsor_message.add_row("")
    sponsor_message.add_row("[u bright_blue link=https://github.com/Avnsh1111/]Github : https://github.com/Avnsh1111/")
    sponsor_message.add_row("")
    sponsor_message.add_row("[u bright_blue link=https://twitter.com/joy_7383/]Twitter : https://twitter.com/joy_7383/")
    sponsor_message.add_row("")
    sponsor_message.add_row("[u bright_blue link=https://instagram.com/avnshrathod/]Instagram : https://twitter.com/avnshrathod/")
    sponsor_message.add_row("")
    message_panel = Panel(
        Align.center(
            Group("\n", Align.center(sponsor_message)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]About Me!",
        border_style="bright_blue",
    )
    return message_panel

# Display the sponsor message
def make_sponsor_message() -> Panel:
    sponsor_message = Table.grid(padding=0)
    sponsor_message.add_column(style="green", justify="center")
    sponsor_message.add_row("[blue] █▀█ █▀▀ █▀▀ █░░ █▀ ▄▄ ▄▀█ █░█ ▀█▀ █▀█ █▀█ █ █░░ █▀█ ▀█▀[/blue]")
    sponsor_message.add_row("[blue] █▀▄ ██▄ ██▄ █▄▄ ▄█ ░░ █▀█ █▄█ ░█░ █▄█ █▀▀ █ █▄▄ █▄█ ░█░[/blue]")
    sponsor_message.add_row("")
    sponsor_message.add_row("Reels-AutoPilot is a powerful GitHub repository that scrapes reels from specified Instagram accounts and shorts from YouTube channels, and automatically posts them to your Instagram account. Keep up with the latest content from your favorite creators and effortlessly share it with your followers. Enhance your Instagram presence and grow your account with Reels-AutoPilot!")
    sponsor_message.add_row("")
    sponsor_message.add_row("[u bright_blue link=https://github.com/Avnsh1111/Instagram-Reels-Scraper-Auto-Poster]Github : https://github.com/Avnsh1111/Instagram-Reels-Scraper-Auto-Poster")

    message_panel = Panel(
        Align.center(
            Group("\n", Align.center(sponsor_message)),
            vertical="top",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Thanks for using Reels-AutoPilot!",
        border_style="bright_blue",
    )

    return message_panel

# Get the reels data from the database
def get_latest_ten_reels():
    session = Session()
    reels = session.query(Reel).order_by(desc(Reel.posted_at)).limit(10).all()
    session.close()
    return reels;

# Get the reels data from the database
def get_reels():
    session = Session()
    reels = session.query(Reel).order_by(desc(Reel.posted_at)).all()
    session.close()
    return reels;

import os
import subprocess
import threading
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich import print
import config as mainConfig
from db import Session, Config
import helpers as Helper
from datetime import datetime
import auth
import sys


def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=20),
        Layout(name="body"),
    )
    layout["body"].split_row(
        Layout(name="links" ),
        Layout(name="logo",ratio=2),
        
    )
    
    return layout

def config_table() -> Panel:

    table = Table(title="",padding=0,show_lines=True,expand=True)
    table.add_column("KEY", style="green", no_wrap=True)
    table.add_column("VALUE", style="magenta")

    table.add_row(" IS_REMOVE_FILES ", ' [green]1=On[/green] ; [red]0=Off[/red] Switch to turn On or Off Files removal ')
    table.add_row(" REMOVE_FILE_AFTER_MINS ", " Duration in minutes to remove files")
    table.add_row(" IS_ENABLED_REELS_SCRAPER ", ' [green]1=On[/green] ; [red]0=Off[/red] Switch to turn On or Off Reels scraper ')
    table.add_row(" IS_ENABLED_AUTO_POSTER ", ' [green]1=On[/green] ; [red]0=Off[/red] Switch to turn On or Off Reels poster ')
    table.add_row(" IS_POST_TO_STORY ", ' [green]1=On[/green] ; [red]0=Off[/red] Switch to turn On or Off Reels auto post on story ')
    table.add_row(" FETCH_LIMIT ", " Screper fetch limit in number Ex. 50")
    table.add_row(" POSTING_INTERVAL_IN_MIN ", " Reels posting interval in minutes Ex. 10 : For every 10 minutes ")
    table.add_row(" SCRAPER_INTERVAL_IN_MIN ", " Reels scraping interval in minutes Ex. 120 : For every 2 hours ")
    table.add_row(" USERNAME ", " Instagram Username ")
    table.add_row(" PASSWORD ", " Instagram Password ")
    table.add_row(" ACCOUNTS ", " Give list of accounts which you want to scrape Ex. carrayminati,totalgaming_official comma separated ")
    table.add_row(" HASTAGS ", " Enter hashtags which you want to add while auto posting ")
    table.add_row(" LIKE_AND_VIEW_COUNTS_DISABLED ", ' [red]1=Disabled[/red] ; [green]0=Enabled[/green] Switch to turn On or Off Likes and view counts ' )
    table.add_row(" DISABLE_COMMENTS ", ' [red]1=Disabled[/red] ; [green]0=Enabled[/green] Switch to turn On or Off comments ' )
    table.add_row(" IS_ENABLED_YOUTUBE_SCRAPING ",  ' [green]1=On[/green] ; [red]0=Off[/red] Switch to turn On or Off YouTube scraper ')
    table.add_row(" YOUTUBE_API_KEY ",  ' Enter Youtube API KEY ')
    table.add_row(" CHANNEL_LINKS ",  " Give list of accounts which you want to scrape Ex.  https://www.youtube.com/@exampleChannleName,https://www.youtube.com/@exampleChannleName comma separated ")
    
    message_panel = Panel(
        Align.left(
            Group("\n", Align.left(table)),
            vertical="top",
        ),
        title="[b red]Configurations",
        border_style="bright_blue",
    )
    
    return message_panel

layout = make_layout()
layout['header'].update(Helper.make_sponsor_message())
layout["logo"].update(config_table())
layout['links'].update(Helper.make_my_information())

print(layout)
print("==========================================================================")
result = input("Press Enter to start the setup...")  

setup = input("Do you want to run the configuration (To update config values) ? (y/n) : ")

if setup == 'y' :

    while True:
        mainConfig.IS_REMOVE_FILES = input("  (IS_REMOVE_FILES) Turn On File Remover After Posting? 1=On;0=Off :")
        if mainConfig.IS_REMOVE_FILES == "0" or mainConfig.IS_REMOVE_FILES == "1":
            Helper.save_config('IS_REMOVE_FILES',mainConfig.IS_REMOVE_FILES)
            break
        else:
            print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

    if mainConfig.IS_REMOVE_FILES == "1" :
    
        while True:
            mainConfig.REMOVE_FILE_AFTER_MINS = input("  (REMOVE_FILE_AFTER_MINS) Define the interval in minutes to remove uploaded files :")
            if mainConfig.REMOVE_FILE_AFTER_MINS.isdigit():
                Helper.save_config('REMOVE_FILE_AFTER_MINS',mainConfig.REMOVE_FILE_AFTER_MINS)
                break
            else:
                print("   [red]Invalid input. Please enter only numeric values.[red]") 


    while True:
        mainConfig.IS_ENABLED_REELS_SCRAPER = input("  (IS_ENABLED_REELS_SCRAPER) Turn On Reels Scraper? 1=On;0=Off :")
        if mainConfig.IS_ENABLED_REELS_SCRAPER == "0" or mainConfig.IS_ENABLED_REELS_SCRAPER == "1":
            Helper.save_config('IS_ENABLED_REELS_SCRAPER',mainConfig.IS_ENABLED_REELS_SCRAPER)
            break
        else:
            print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

    if mainConfig.IS_ENABLED_REELS_SCRAPER == "1" :

        while True:
            mainConfig.FETCH_LIMIT = input("  (FETCH_LIMIT) Define number of latest reels to be scrape from each account :")
            if mainConfig.IS_ENABLED_REELS_SCRAPER.isdigit():
                Helper.save_config('FETCH_LIMIT',mainConfig.FETCH_LIMIT)
                break
            else:
                print("   [red]Invalid input. Please enter only numeric values.[red]") 

        while True:
            mainConfig.SCRAPER_INTERVAL_IN_MIN = input("  (SCRAPER_INTERVAL_IN_MIN) Define scraper interval in minuters :")
            if mainConfig.SCRAPER_INTERVAL_IN_MIN.isdigit():
                Helper.save_config('SCRAPER_INTERVAL_IN_MIN',mainConfig.SCRAPER_INTERVAL_IN_MIN)
                break
            else:
                print("   [red]Invalid input. Please enter only numeric values.[red]") 
            
    while True:
        mainConfig.IS_ENABLED_AUTO_POSTER = input("  (IS_ENABLED_AUTO_POSTER) Turn On Reels Autoposter? 1=On;0=Off :")
        if mainConfig.IS_ENABLED_AUTO_POSTER == "0" or mainConfig.IS_ENABLED_AUTO_POSTER == "1":
            Helper.save_config('IS_ENABLED_AUTO_POSTER',mainConfig.IS_ENABLED_AUTO_POSTER)
            break
        else:
            print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

    if mainConfig.IS_ENABLED_AUTO_POSTER == "1" :

        while True:
            mainConfig.POSTING_INTERVAL_IN_MIN = input("  (POSTING_INTERVAL_IN_MIN) Define posting interval in minutes :")
            if mainConfig.IS_ENABLED_REELS_SCRAPER.isdigit():
                Helper.save_config('POSTING_INTERVAL_IN_MIN',mainConfig.POSTING_INTERVAL_IN_MIN)
                break
            else:
                print("   [red]Invalid input. Please enter only numeric values.[red]") 

    

    while True:
        mainConfig.IS_POST_TO_STORY = input("  (IS_POST_TO_STORY) Turn On post reels into stroy? 1=On;0=Off :")
        if mainConfig.IS_POST_TO_STORY == "0" or mainConfig.IS_POST_TO_STORY == "1":
            Helper.save_config('IS_POST_TO_STORY',mainConfig.IS_POST_TO_STORY)
            break
        else:
            print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

    


    if mainConfig.IS_ENABLED_AUTO_POSTER == "1"  or mainConfig.IS_ENABLED_REELS_SCRAPER == "1":

        while True:
            mainConfig.USERNAME = input("  (USERNAME) Enter Instagram Username :")
            if mainConfig.USERNAME != "":
                Helper.save_config('USERNAME',mainConfig.USERNAME)
                break
            else:
                print("  [red]Invalid input. Please enter username.[/red]")

        while True:
            mainConfig.PASSWORD = input("  (PASSWORD) Enter Instagram Password :")
            if mainConfig.PASSWORD != "":
                Helper.save_config('PASSWORD',mainConfig.PASSWORD)
                break
            else:
                print("  [red]Invalid input. Please enter password.[/red]")

        try:
            os.remove('session.json')
            print(f"File session.json has been removed successfully.")
        except OSError as e:
            print(f"Error: {e}")

        auth.login()

        mainConfig.ACCOUNTS = input("  (ACCOUNTS) Enter list of username which you want to scrape (comma separated) :")
        Helper.save_config('ACCOUNTS',mainConfig.ACCOUNTS)

        mainConfig.HASTAGS = input("  (HASTAGS) Enter hashtags which you want to add while posting :")
        Helper.save_config('HASTAGS',mainConfig.HASTAGS)

        while True:
            mainConfig.LIKE_AND_VIEW_COUNTS_DISABLED = input("  (LIKE_AND_VIEW_COUNTS_DISABLED) Enter 1 to Disable or 0 to enable like and views counts :")
            if mainConfig.LIKE_AND_VIEW_COUNTS_DISABLED == "0" or mainConfig.LIKE_AND_VIEW_COUNTS_DISABLED == "1":
                Helper.save_config('LIKE_AND_VIEW_COUNTS_DISABLED',mainConfig.LIKE_AND_VIEW_COUNTS_DISABLED)
                break
            else:
                print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

        while True:
            mainConfig.DISABLE_COMMENTS = input("  (DISABLE_COMMENTS) Enter 1 to Disable or 0 to enable comments :")
            if mainConfig.DISABLE_COMMENTS == "0" or mainConfig.DISABLE_COMMENTS == "1":
                Helper.save_config('DISABLE_COMMENTS',mainConfig.DISABLE_COMMENTS)
                break
            else:
                print("  [red]Invalid input. Please enter only 0 or 1.[/red]")


    while True:
        mainConfig.IS_ENABLED_YOUTUBE_SCRAPING = input("  (IS_ENABLED_YOUTUBE_SCRAPING) Turn On YouTube Shorts Scraper? 1=On;0=Off :")
        if mainConfig.IS_ENABLED_YOUTUBE_SCRAPING == "0" or mainConfig.IS_ENABLED_YOUTUBE_SCRAPING == "1":
            Helper.save_config('IS_ENABLED_YOUTUBE_SCRAPING',mainConfig.IS_ENABLED_YOUTUBE_SCRAPING)
            break
        else:
            print("  [red]Invalid input. Please enter only 0 or 1.[/red]")

    if mainConfig.IS_ENABLED_YOUTUBE_SCRAPING  == "1" :

        mainConfig.YOUTUBE_API_KEY = input("  (YOUTUBE_API_KEY) Enter Youtube API KEY :")
        Helper.save_config('YOUTUBE_API_KEY',mainConfig.YOUTUBE_API_KEY)

        mainConfig.CHANNEL_LINKS = input("  (CHANNEL_LINKS) Enter channel links to scrape (comma separated) :")
        Helper.save_config('CHANNEL_LINKS',mainConfig.CHANNEL_LINKS)


python_executable_path = sys.executable
os.system(python_executable_path+" app.py 1")
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from rich import print
import config
import helpers as Helper
import os

SESSION_FILE = 'session.json'

# Login function
def login() :
    print("   [green] Initializing login... [/green]")
    api = Client()
    api.delay_range = [1, 3]
    Helper.load_all_config()

    
    if os.path.exists(SESSION_FILE):
        print("   [green] Logging with previous session... [/green]")
        api.load_settings(SESSION_FILE)
        api.login (config.USERNAME, config.PASSWORD) # this doesn't actually login using username/password but uses the session
        api.dump_settings(SESSION_FILE)
        api.get_timeline_feed()
        return api
        
    else :
        print("   [green] Logging with username and password... [/green]")
        api.login(config.USERNAME, config.PASSWORD)
        api.dump_settings(SESSION_FILE)
        api.get_timeline_feed()
        return api
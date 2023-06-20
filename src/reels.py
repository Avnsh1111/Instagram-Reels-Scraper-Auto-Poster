from instagrapi import Client
from db import Session, Reel, ReelEncoder
import json
import config
import time
import auth
import helpers as Helper
from helpers import print


#Function to fetch reel from given account
def get_reels(account,api):
    user_id = api.user_id_from_username(account)
    medias = api.user_medias(user_id, config.FETCH_LIMIT)
    reels = [item for item in medias if (item.product_type == 'clips' , item.media_type == 2)]  # Filter for reels (product_type == 3)
    return reels

#Function to get file name from URL
def get_file_name_from_url(url):
    path = url.split('/')
    filename = path[-1]
    return filename.split('?')[0]


#Function to get file path
def get_file_path(file_name):
    return config.DOWNLOAD_DIR + file_name


#Magic Starts Here
def main(api):
    Helper.load_all_config()
    session = Session()
    for account in config.ACCOUNTS:

        reels_by_account = get_reels(account,api)

        for reel in reels_by_account:
            #print(f"Reel ID: {reel.id}, Caption: {reel.caption_text}, Url : {reel.video_url}")
            if reel.video_url != None :
                try :
                    print('------------------------------------------------------------------------------------')
                    print('Checking if reel : '+reel.code+' already downloaded')
                    exists = session.query(Reel).filter_by(code=reel.code).first()
                    #exists = False
                    if not exists:
                        filename = get_file_name_from_url(reel.video_url)
                        filepath = get_file_path(filename)
                        
                        print('Downloading Reel From : ' +account+ ' | Code : '+ reel.code)
                        api.video_download_by_url(reel.video_url, folder=config.DOWNLOAD_DIR)
                        print('Downloaded Reel Code : ' +reel.code+ ' | Path : '+filepath)
                        print('<---------Database Insert Start--------->')

                        reel_db = Reel(
                                    post_id=reel.id,
                                    code=reel.code,
                                    account = account,
                                    caption = reel.caption_text,
                                    file_name = filename,
                                    file_path = filepath,
                                    data = json.dumps(reel, cls=ReelEncoder),
                                    is_posted = False,
                                    #posted_at = NULL
                                    )
                        session.add(reel_db)
                        session.commit()
                        
                        print('Inserting Record...')
                        #print('Insert Reel Record : ' + json.dumps(reel, cls=ReelEncoder) )
                        print('<---------Database Insert End--------->')
                    print('------------------------------------------------------------------------------------')
                except :
                    # Do Nothing
                    pass
                
    session.close()
    # time.sleep(int(config.SCRAPER_INTERVAL_IN_MIN)*60)
    # main(api)

# if __name__ == "__main__":
#     api = auth.login()
#     main(api)
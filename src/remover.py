import os
from db import Session, Reel, ReelEncoder
import config
import time
import helpers as Helper
from helpers import print

def remove_file(file_path):
    try:
        # Remove the file
        os.remove(file_path)
        print("File removed successfully.")
    except FileNotFoundError:
        #print("File not found.")
        pass
    except PermissionError:
        print("Permission denied: unable to remove the file.")
        pass
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pass

def main():
    Helper.load_all_config()
    session = Session()
    reels = session.query(Reel).filter_by(is_posted=True).all()

    for reel in reels:
        remove_file(reel.file_path)

    #time.sleep(int(config.REMOVE_FILE_AFTER_MINS) * 60)


# if __name__ == "__main__":
    
#     main()
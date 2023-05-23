import os
from src.db import Session, Reel, ReelEncoder

def remove_file(file_path):
    try:
        # Remove the file
        os.remove(file_path)
        print("File removed successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied: unable to remove the file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    session = Session()
    reels = session.query(Reel).filter_by(is_posted=True).all()

    for reel in reels:
        remove_file(reel.file_path)
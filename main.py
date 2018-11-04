import os
from upload import upload_blob
from parser import *

def update_videos(username, password):
    get_wav(get_videos(username, password))
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                upload_blob("audioforhtm", file, file)

if __name__=='__main__':
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    update_videos(username, password)

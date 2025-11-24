import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = "AIzaSyCU3h06DwYZzq0erB5puk5FABJujZka6kQ"

CHANNEL_HANDEL = "MrBeast"

def get_playlist_id():

    try:
        #Url of the channel list API
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDEL}&key={API_KEY}"

        #getting a responce from the API
        response = requests.get(url)

        response.raise_for_status()
        #print(response) #this will print the resonse of the API.

        data = response.json()   #Taking the response data in the variable

        #print(json.dumps(data,indent=4))

        Channel_items = data["items"][0]  #List of the Channel Items

        # Getting the Playlist id
        Channel_playlistID = Channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(Channel_playlistID)

        return Channel_playlistID

    # this will raise an exception whenever it will find any
    except requests.exceptions.RequestException as e:
        raise e

if __name__== "__main__": 
    get_playlist_id()

#if we want to run it as script then this main will be executed 
#BUT if will want to run it as a module then you need to sepecify the file name instead of main or the else will be executed.

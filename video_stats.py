import requests
import json
import os
from dotenv import load_dotenv  

load_dotenv(dotenv_path="./.env") #Getting the Secrets from .env file i.e API Keys.
API_KEY = os.getenv("API_KEY")  # reads .env and sets environment variables

CHANNEL_HANDEL = "MrBeast"  #Youtube Channel name.

def get_playlist_id(): #Defination of tyhe function to get the Playlist id from the MR. Beast youtube Channel.

    try:
        #Url of the channel list/ Playlist API
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
        #print(Channel_playlistID)

        return Channel_playlistID

    # this will raise an exception whenever it will find any
    except requests.exceptions.RequestException as e:
        raise e


maxResults=50  #For the max number of the videos in a lists.

def get_video_id(playlistId):  #Definition of the function which gets you the Video id of the playlist that we are getting as an input.

    video_ids = [] #creating a list for all video id that we are going to get from APIs.

    pageToken = None  #Initially set to NONE.

    #This is the base URL to fetch the Video ids from Mr. Beast Youtube Channel.
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

    try:

        while True:
            url = base_url
            if(pageToken):
                url += f"&pageToken={pageToken}"
            
            #getting a responce from the API
            response = requests.get(url)

            response.raise_for_status()
            #print(response) #this will print the resonse of the API.

            data = response.json()   #Taking the response data in the variable
            #print(json.dumps(data,indent=4))

            for item in data.get('items',[]):  #the loop will pull all the videid from the response JSON.The empty list is used in the variable because if we dont have the items , the loop will not show an error and it will work.
                video_id = item['contentDetails']['videoId']  #pulling ythe videoid from the JSON data coming as a response from the API.
                video_ids.append(video_id)   #this will append all the videoid in the list.

            if not pageToken:  #exit condition from the above loop.
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e




if __name__== "__main__": 
    playlistId = get_playlist_id()  #Function call to get the playlist id.
    print(playlistId) #Printing the Playlistid
    get_video_id(playlistId) #Function call to get the Video ids.
    #print(get_video_id(playlistId))   #Printing the Video ids

#if we want to run it as script then this main will be executed 
#BUT if will want to run it as a module then you need to sepecify the file name instead of main or the else will be executed.

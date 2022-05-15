import json
import pandas as pd
import requests

key = <yt_data_api>

ytdata = pd.DataFrame()
ytchannel = ["sonymusicindiaSME","sonypalindia","marvel"]

def retrive_data(url):

    json_url = requests.get(url)
    value = json.loads(json_url.text)
    
    return value

for i in ytchannel:
    username = i
    
    url = f'https://www.googleapis.com/youtube/v3/channels?key={key}&forUsername={username}&part=id'
    data = retrive_data(url)
    
    channel_id = data['items'][0]['id']
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={key}'
    data = retrive_data(url)
    
    details = data['items'][0]['statistics']
    
    url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20"
    
    data = retrive_data(url)
    
    details['channelTitle'] = data['items'][0]['snippet']['channelTitle']
    channel_statistics = pd.DataFrame([details])
    
    ytdata = ytdata.append(channel_statistics)
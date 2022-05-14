import json
import pandas as pd
import requests

channel_id = <channel_id>
key = <yt_data_api>

url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={key}'

json_url = requests.get(url)
data = json.loads(json_url.text)

try:
    details = data['items'][0]['statistics']
except KeyError:
    print('Could not get channel statistics')
    details = {}

url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20"

json_url = requests.get(url)
data = json.loads(json_url.text)

details['channelTitle'] = data['items'][0]['snippet']['channelTitle']
channel_statistics = pd.DataFrame([details])
import re
import ast
import json
import requests
import pandas as pd
from collections import Counter

key = <yt_data_api>

ytdata = pd.DataFrame()
ytchannel = ["sonymusicindiaSME","sonypalindia","marvel","SuperwomanVlogs","TseriesKannada"]

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
    
    url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=30"
    
    data = retrive_data(url)
    
    details['channelTitle'] = data['items'][0]['snippet']['channelTitle']
    channel_statistics = pd.DataFrame([details])
    
    video = []

    for vid in data['items']:
        video.append(vid['snippet']['title'])

    channel_statistics['recentVideo'] = str(video) 
    
    ytdata = ytdata.append(channel_statistics,ignore_index=False)
    
ytdata.reset_index(drop=True,inplace=True)

# Data Analysis

highest = ytdata[ytdata['subscriberCount'] == ytdata['subscriberCount'].max()].index[0]
print("Highest subscriber count channel title: {}\n".format(ytdata["channelTitle"][highest]))

lowest = ytdata[ytdata['subscriberCount'] == ytdata['subscriberCount'].min()].index[0]
print("Lowest subscriber count channel title: {}\n".format(ytdata["channelTitle"][lowest]))

highest = ytdata[ytdata['viewCount'] == ytdata['viewCount'].max()].index[0]
print("Highest view count channel title: {}\n".format(ytdata["channelTitle"][highest]))

lowest = ytdata[ytdata['viewCount'] == ytdata['viewCount'].min()].index[0]
print("Lowest view count channel title: {}\n".format(ytdata["channelTitle"][lowest]))

for i in range(len(ytdata)):

    results = ytdata['recentVideo'][i]
    results = ast.literal_eval(results)
    results = "".join(results)
    results = re.sub('[^A-Za-z0-9]+', ' ', results)
    results = results.split()
    
    CounterVariable = Counter(results)
    
    most_occur = CounterVariable.most_common(1)[0][0]
    
    ytdata.loc[ytdata.index == i, 'frequentWord'] = most_occur
    
    print("'{}' is the most frequent word used by {}\n".format(most_occur,ytdata['channelTitle'][i]))
    
branding = ytdata.apply(lambda x:x["channelTitle"] if x["frequentWord"] in x["channelTitle"] else '', axis=1).tolist()   
branding = [x.strip().title() for x in branding if x != '']
branding = ", ".join(branding)
print("The YouTube channels '{}' use their own title the most!".format(branding))
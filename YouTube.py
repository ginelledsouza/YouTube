import re
import ast
import json
import requests
import pandas as pd
from collections import Counter
import googleapiclient.discovery

key = <yt_data_api>
api_service_name = "youtube"
api_version = "v3"

####################################### [Searching Channels] #######################################

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

highest = ytdata[ytdata['videoCount'] == ytdata['videoCount'].max()].index[0]
print("Highest video count channel title: {}\n".format(ytdata["channelTitle"][highest]))

lowest = ytdata[ytdata['videoCount'] == ytdata['videoCount'].min()].index[0]
print("Lowest video count channel title: {}\n".format(ytdata["channelTitle"][lowest]))

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

####################################### [Searching Popular Videos] #######################################

def searchvid(keyword):
    
    keyword = keyword.strip().lower()
    
    viddata = pd.DataFrame()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = key)
    
    videos_ids = youtube.search().list(part="id",type='video',regionCode="IN",order="relevance",
                                       q=keyword,maxResults=50,fields="items(id(videoId))").execute()
    
    keys, values = zip(*videos_ids.items())
    values = values[0]
    
    for i in values:
            
        vid = i["id"]["videoId"]
        stat = youtube.videos().list(part="statistics,contentDetails",id=vid,fields="items(statistics," + "contentDetails(duration))").execute()
        print(vid)
        
        video_statistics = stat['items'][0]["contentDetails"]
        Addons = stat['items'][0]["statistics"]
        
        video_statistics.update(Addons)
        
        video_statistics = pd.DataFrame(video_statistics,index=[0])
        
        viddata = viddata.append(video_statistics,ignore_index=False)
        
    viddata.reset_index(drop=True,inplace=True)
    viddata.rename(columns={"duration":"_id"},inplace=True)
    
    return viddata

keyword = "Fashion"
Video = searchvid(keyword)
import json
import pandas as pd
import requests
from tqdm import tqdm

channel_id = <channel_id>
key = <yt_data_api>

url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={key}'
pbar = tqdm(total=1)

json_url = requests.get(url)
data = json.loads(json_url.text)
try:
    data = data['items'][0]['statistics']
except KeyError:
    print('Could not get channel statistics')
    data = {}

channel_statistics = pd.DataFrame([data])
pbar.update()
pbar.close()
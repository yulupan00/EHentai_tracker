
import json

file_path = "gdata.json"

with open(file_path, "r") as json_file:
    data = json.load(json_file)

print(data['9'])

l = 0
for entry in data:
    gid = entry.get("gid")
    token = entry.get("token")
    l+=1
print(l)
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

import time

url_list = []
page_range = 20

for i in tqdm(range(1, page_range)):
    url = "https://e-hentai.org/?f_srdd=4&advsearch=1&range={}".format(i)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for td in soup.find_all('td', class_='gl3c glname'):
            a_tag = td.find('a')
            if a_tag:
                href = a_tag.get('href')
                url_list.append(href)
    else:
        print("fail")
        
    time.sleep(2.5)

l = []
for url in url_list:
    gid = url.split("/")[-3]
    token = url.split("/")[-2]
    l.append([gid, token])

df = pd.DataFrame(l, columns=["gid", "token"])

csv_filename = 'hentai_data.csv'
df.to_csv(csv_filename, index=False)
'''
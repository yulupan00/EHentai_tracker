import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

import random
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

api_url = "https://api.e-hentai.org/api.php"

def sleepSome():
    sleep_time = random.uniform(1, 10)
    time.sleep(sleep_time)

def getRaw():
    url_list = []
    page_range = 20
    for i in tqdm(range(1, page_range + 1)):
        url = "https://e-hentai.org/?f_srdd=4&advsearch=1&range={}".format(i)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for td in soup.find_all('td', class_='gl3c glname'):
                a_tag = td.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    url_list.append(href)
        else:
            print("fail")
        sleepSome()

    l = []
    for url in url_list:
        gid = url.split("/")[-3]
        token = url.split("/")[-2]
        l.append([gid, token])

    df = pd.DataFrame(l, columns=["gid", "token"])

    csv_filename = 'hentai_data_20.csv'
    df.to_csv(csv_filename, index=False)

def getDownloadCount(gid, token):
    url = f"https://e-hentai.org/gallerytorrents.php?gid={gid}&t={token}"
    response = requests.get(url, headers=headers)
    total_downloads = 0
    valid = True
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        td_elements = soup.find_all('td', style="width:100px; text-align:center")
        if len(td_elements) == 0:
            valid = False
        for td in td_elements:
            if "Downloads:" in td.text:
                downloads = int(td.text.split(":")[1])
                total_downloads += downloads
        print("Total Downloads:", total_downloads)
    return total_downloads, valid

def getDownload():
    df = pd.read_csv('hentai_data_20.csv')
    l = []
    for index, row in df.iterrows():
        gid = row['gid']
        token = row['token']
        download, valid = getDownloadCount(gid, token)
        if valid:
            l.append([gid, token, download])
        sleepSome()
    df_result = pd.DataFrame(l, columns=["gid", "token", "downloads"])
    df_result.to_csv("hentai_data.csv", index=False)

def getTags(gid, token):
    payload = {
        "method": "gdata",
        "gidlist": [
            [int(gid), token]
        ],
        "namespace": 1
    }

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        json_data = response.json()
        tags = json_data["gmetadata"][0]["tags"]
        print(tags)
    return tags

def getAllTags():
    df = pd.read_csv('hentai_data.csv')
    l = []

    for index, row in df.iterrows():
        gid = row['gid']
        token = row['token']
        download = row['downloads']
        tag = getTags(gid, token)
        l.append([gid, token, download, tag])
        time.sleep(random.uniform(1, 10))

    df_result = pd.DataFrame(l, columns=["gid", "token", "downloads", "tag"])
    df_result.to_csv("hentai_data_all.csv", index=False)

def getTagWithDownloads():
    df = pd.read_csv("hentai_data_all.csv")

    tag_dict = {} #Format: tag -> download_count, category, num_appearance

    for index, row in df.iterrows():
        tags = eval(row["tag"])
        for tag in tags:
            split = tag.split(':')
            if(len(split) == 1):
                split = ['other', split[0]]
            category, name = split
            if name in tag_dict:
                tag_dict[name][0] += row['downloads']
                tag_dict[name][2] += 1
            else:
                tag_dict[name] = [row['downloads'], category, 1]

    sorted_tags = dict(sorted(tag_dict.items(), key=lambda x: x[1], reverse=True))

    res_df = pd.DataFrame.from_dict(sorted_tags, orient='index', columns=["download_count", "category", "num_appearance"]).rename_axis("tag").reset_index()
    res_df.to_csv("hentai_data_tag.csv", index=False)


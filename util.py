import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm

import random
import time

api_url = "https://api.e-hentai.org/api.php"
headers = {}
min_rateing = 4

#Sleep between request websites to prevent getting blocked
def sleepSome():
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

#Web scrap e-hentai.org and get the every gallery on the pages
def getRaw(start_page = 1, page_range = 20, save = False):
    if(start_page == 0):
        start_page = 1
    url_list = []
    url = "https://e-hentai.org/?f_srdd={}&f_sto=on&advsearch=1&range={}".format(min_rateing,start_page)
    for i in tqdm(range(start_page, page_range + 1)):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for td in soup.find_all('td', class_='gl3c glname'):
                a_tag = td.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    url_list.append(href)
            url = soup.find('a', id='unext')['href']
        else:
            print("fail")
        sleepSome()
    new_data = []
    for url in url_list:
        gid = url.split("/")[-3]
        token = url.split("/")[-2]
        new_data.append([gid, token])

    df = pd.DataFrame(new_data, columns=["gid", "token"])
    if save:
        df.to_csv('hentai_data.csv', index=False)
    return df

#Get the tag of one gid and token
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
        try:
            json_data = response.json()
            tags = json_data["gmetadata"][0]["tags"]
            title = json_data["gmetadata"][0]["title"]
            torrent_count = int(json_data["gmetadata"][0]["torrentcount"])
            category = json_data["gmetadata"][0]["category"]
            valid = len(tags) > 0 and torrent_count > 0
            tqdm.write(str(tags[:5]))
        except:
            tqdm.write("Failure!")
            return "","","", False
    return tags, title, category, valid

#Get every tag from a list of gid and token
def getAllTags(df = None, save = False):
    if df is None:
        df = pd.read_csv('hentai_data.csv')
    df["tag"] = np.nan
    df["title"] = ""
    df["category"] = ""

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        gid = row['gid']
        token = row['token']
        tag, title, category, valid = getTags(gid, token)
        if valid:
            df.at[index,'tag'] = str(tag)
            df.at[index,'title'] = title
            df.at[index,'category'] = category
        else:
            tqdm.write("Not good: {}".format(title))
        sleepSome()
    if save:
        df.to_csv("hentai_data.csv", index=False)
    df = df.dropna()
    return df

#Get the total download count of a gid and token
def getDownloadCount(gid, token):
    url = "https://e-hentai.org/gallerytorrents.php?gid={}&t={}".format(gid, token)
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
    return int(total_downloads), valid

#Get the download count from a list of gid and token
def getDownload(df = None, save = True):
    if df is None:
        df = pd.read_csv('hentai_data.csv')
    df["downloads"] = np.nan
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        gid = row['gid']
        token = row['token']
        download, valid = getDownloadCount(gid, token)
        tqdm.write("{} Total Downloads: {}".format(row['title'][:20], download))
        df.at[index,'downloads'] = int(download)
        sleepSome()
    df = df.dropna()
    if save:
        df.to_csv("hentai_data.csv", index=False)
    return df

#Associate each tag with its total download
def getTagWithDownloads(df = None, save = True):
    if df is None:
        df = pd.read_csv("hentai_data.csv")

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
    if save:
        res_df.to_csv("hentai_data_tag.csv", index=False)
    return res_df

#List the galleries with a certain tag
def listGalleryWithTag(tag):
    df = pd.read_csv("hentai_data.csv")
    l = []
    for index, row in df.iterrows():
        if tag in row["tag"]:
            print("Title: {}, GID: {}, Token: {}".format(row["title"], row["gid"], row["token"]))
            l.append([row["gid"], row["token"]])
    return l

#Get one random image from the first page of a gallery
def previewPage(gid, token):
    url = "https://e-hentai.org/g/{}/{}".format(gid, token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_links = soup.find_all('a')
        images = []
        for image in image_links:
            href = image.get('href')
            if href is not None and "{}-".format(gid) in href:
                images.append(href)
        if len(images) == 0:
            print("No Image Available")
        sleepSome()
        select = random.choice(images)
        response = requests.get(select, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_link = soup.find('img', {"id": 'img'})
        image_url = image_link.get("src")
        sleepSome()
        response = requests.get(image_url, headers=headers)
        image_data = response.content
        local_file_path = "{}_preview.jpg".format(gid)
        with open(local_file_path, 'wb') as file:
            file.write(image_data)

#Get the thumbnail of a gallery
def getThumbNail(gid, token):
    payload = {
        "method": "gdata",
        "gidlist": [
            [int(gid), token]
        ],
        "namespace": 1
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        try:
            json_data = response.json()
            thumb = json_data["gmetadata"][0]["thumb"]
            sleepSome()
            image = requests.get(thumb, headers=headers)
            filename = "{}_thumbnail.jpg".format(gid)
            with open(filename, 'wb') as f:
                f.write(image.content)
            print("Image saved as {}".format(filename))
        except:
            print("Failed!")

#Get the top download gallery with tag/catergory query
def qualitySearch(queries):
    df = pd.read_csv("hentai_data.csv")
    for query in queries:
        df = df[df[query].str.contains(queries[query], case=False, na=False)]
    sorted_df = df.sort_values(by='downloads', ascending=False)
    print(sorted_df.head())

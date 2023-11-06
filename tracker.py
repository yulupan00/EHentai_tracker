import requests
import json
from bs4 import BeautifulSoup

api_url = "https://api.e-hentai.org/api.php"

gid = "2231376"
token = "a7584a5932"
#gid = "9"
#token = "e56264c60c"


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
            
     

def getDownloadCount(gid, token):
    url = f"https://e-hentai.org/gallerytorrents.php?gid={gid}&t={token}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        td_elements = soup.find_all('td', style="width:100px; text-align:center")

        total_downloads = 0

        for td in td_elements:
            if "Downloads:" in td.text:
                downloads = int(td.text.split(":")[1])
                total_downloads += downloads

        print("Total Downloads:", total_downloads)



print(getTags(gid, token))
# E-HENTAI TRACKER
Track the most recent popular quality posts on the e-hentai.org based on the download counts of the torrent files.

This script scrap the most recent n pages of posts with 4 star + rating on e-hentai, then associate each tag with total download count. The most popular tags will be displayed.

To prevent getting blocked by the website, change the headers in main.py. The script runs slow since it will sleep for some seconds after each request to e-hentai.org

Example plots:

![Alt text](images/overall.png)

![Alt text](images/character.png)

![Alt text](images/parody.png)
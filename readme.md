# E-HENTAI TRACKER
Track the most recent popular quality posts on the e-hentai.org based on the download counts of the torrent files.

This script scrap the most recent n pages of posts with 4 star + rating on e-hentai, then associate each tag with total download count. The most popular tags will be displayed.

To prevent getting blocked by the website, change the headers in main.py. The script runs slow since it will sleep for some seconds after each request to e-hentai.org

Some data gathered from E-hentai.org. Only galleries with 3 stars ratings are included. Link: https://mega.nz/file/bZZXCBgQ#vQwcgOto5_Z66GEl8LLmiZQjvWU8fSkicAnP59f2Mx0

Example plots:

![Alt text](images/overall.png)

![Alt text](images/character.png)

![Alt text](images/parody.png)

![Alt text](images/category_plot.png)
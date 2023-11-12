import util
from plot import *

#Replace with "my user agent". Type that in Google and copy the result
headers = {
    'User-Agent': ''
}

util.headers = headers

#Prepare data
df = util.getRaw(start_page = 1, page_range = 100)
df = util.getAllTags(df)
df = util.getDownload(df)
res_df = util.getTagWithDownloads(df)

print("---------")

res_df = util.getTagWithDownloads()
plotOverall()

#Example use
util.getThumbNail(2716694,"929e75127b")
util.qualitySearch({"tag": "genshin impact", "category": "Doujinshi"})
import util, plot

#Replace with "my user agent". Type that in Google and copy the result
headers = {
    'User-Agent': ''
}

util.headers = headers

df = util.getRaw(start_page = 1, page_range = 50)
df = util.getAllTags(df)
df = util.getDownload(df)
res_df = util.getTagWithDownloads(df)

print("---------")

res_df = util.getTagWithDownloads()
plot.plotOverall()
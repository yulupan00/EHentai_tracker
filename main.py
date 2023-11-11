import util, plot

#Replace with "my user agent". Type that in Google and copy the result
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

util.headers = headers

df = util.getRaw(start_page = 1, page_range = 100)
df = util.getAllTags(df)
df = util.getDownload(df)
res_df = util.getTagWithDownloads(df)

print("---------")

res_df = util.getTagWithDownloads()
plot.plotOverall()
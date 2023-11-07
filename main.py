import util, plot

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

util.headers = headers

util.getRaw(page_range = 2)
util.getDownload()
util.getAllTags()
util.getTagWithDownloads()

plot.plotOverall()

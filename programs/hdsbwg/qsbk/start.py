
from scrapy import cmdline

#cmdline.execute("scrapy crawl qsbk_spider".split())

cmdline.execute(["scrapy",'crawl','handan'])
cmdline.execute(["scrapy",'crawl','qsbk_spider'])
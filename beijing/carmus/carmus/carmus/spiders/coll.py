import scrapy


class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.automuseum.org.cn/']
    start_urls = ['http://http://www.automuseum.org.cn//']

    def parse(self, response):
        pass

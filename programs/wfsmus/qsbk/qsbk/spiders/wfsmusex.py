import scrapy


class WfsmusexSpider(scrapy.Spider):
    name = 'wfsmusex'
    allowed_domains = ['http://www.wfsbwg.com']
    start_urls = ['http://http://www.wfsbwg.com/']

    def parse(self, response):
        pass

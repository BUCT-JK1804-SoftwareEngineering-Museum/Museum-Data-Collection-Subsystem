import scrapy


class HqmusexSpider(scrapy.Spider):
    name = 'hqmusex'
    allowed_domains = ['http://www.hqbwy.org.cn']
    start_urls = ['http://http://www.hqbwy.org.cn/']

    def parse(self, response):
        pass

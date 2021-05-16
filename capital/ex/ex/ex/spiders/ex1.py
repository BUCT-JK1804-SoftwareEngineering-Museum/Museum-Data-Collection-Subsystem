import scrapy
from ..items import ExItem

class Ex1Spider(scrapy.Spider):
    name = 'ex1'
    allowed_domains = ['http://www.capitalmuseum.org.cn/']
    start_urls = ['http://www.capitalmuseum.org.cn/']

    def parse(self, response):
        pass

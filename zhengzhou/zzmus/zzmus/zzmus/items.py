# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZzmusItem(scrapy.Item):
    id = scrapy.Field()
    mus_id = scrapy.Field()
    mus_name = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    era = scrapy.Field()
    introduction = scrapy.Field()
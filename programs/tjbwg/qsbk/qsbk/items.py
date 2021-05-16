# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QsbkItem(scrapy.Item):
    id = scrapy.Field()
    mus_id = scrapy.Field()
    name = scrapy.Field()
    era = scrapy.Field()
    introduction = scrapy.Field()
    mus_name=scrapy.Field()
    image = scrapy.Field()

class DtxsexItem(scrapy.Item):
    exh_id=scrapy.Field()
    exh_name=scrapy.Field()
    mus_id=scrapy.Field()
    mus_name=scrapy.Field()
    exh_info=scrapy.Field()
    exh_picture=scrapy.Field()
    exh_time=scrapy.Field()



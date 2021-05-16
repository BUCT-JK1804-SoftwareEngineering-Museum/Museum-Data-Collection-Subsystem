# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QsbkItem(scrapy.Item):
    col_id = scrapy.Field()
    mus_id = scrapy.Field()
    col_name = scrapy.Field()
    col_era = scrapy.Field()
    col_info = scrapy.Field()
    mus_name = scrapy.Field()
    col_picture = scrapy.Field()

class QsbkexItem(scrapy.Item):
    exh_id=scrapy.Field()
    exh_name=scrapy.Field()
    mus_id=scrapy.Field()
    mus_name=scrapy.Field()
    exh_info=scrapy.Field()
    exh_picture=scrapy.Field()
    exh_time=scrapy.Field()



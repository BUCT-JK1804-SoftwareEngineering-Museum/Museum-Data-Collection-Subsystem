# -*- coding = utf-8 -*-
# @Time : 2021/5/4 23:02
# @Author : waynemars
# @File : item.py
# @Software : PyCharm
import scrapy


class MusexItem(scrapy.Item):
    id = scrapy.Field()
    mus_id = scrapy.Field()
    mus_name = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    era = scrapy.Field()
    introduction = scrapy.Field()
# -*- coding = utf-8 -*-
# @Time : 2021/5/6 16:03
# @Author : waynemars
# @File : exitems.py
# @Software : PyCharm
import scrapy


class CyexItem(scrapy.Item):
    id = scrapy.Field()
    mus_id = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()
    mus_name = scrapy.Field()
    image = scrapy.Field()
    time = scrapy.Field()
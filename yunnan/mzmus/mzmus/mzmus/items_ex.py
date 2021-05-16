# -*- coding = utf-8 -*-
# @Time : 2021/5/8 19:49
# @Author : waynemars
# @File : items_ex.py
# @Software : PyCharm
import scrapy


class MzexItem(scrapy.Item):
    id = scrapy.Field()
    mus_id = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()
    mus_name = scrapy.Field()
    image = scrapy.Field()
    time = scrapy.Field()
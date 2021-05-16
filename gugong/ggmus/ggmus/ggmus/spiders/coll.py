# -*- coding = utf-8 -*-
# @Time : 2021/5/11 17:01
# @Author : waynemars
# @File : coll.py
# @Software : PyCharm
import scrapy
from bs4 import BeautifulSoup
from pip._vendor import requests

from ..items import GgmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    # allowed_domains = ['https://zm-digicol.dpm.org.cn/']
    start_urls = ['https://zm-digicol.dpm.org.cn/cultural/list']
    base_url = "https://zm-digicol.dpm.org.cn/"

    i = 2
    mus_name_num = '故宫博物院'
    id_num = 1
    mus_ida = 1101
    next_url = []

    def parse(self, response):
        qtqs = response.xpath("//div[@class='table_box']/div")
        # print('#' * 40)
        # print(qtqs)
        # print('#' * 40)
        for qtq in qtqs:
            fur = qtq.xpath(".//div[1]").get()
            era = qtq.xpath(".//div[3]").get()
            print('#' * 40)
            print(fur)
            print(era)
            print('#' * 40)
            # yield scrapy.Request(fur, callback=self.parse_detail, dont_filter=True,
            #                      meta={"fur": fur, "era":era})

        next = self.base_url + "cultural/list?page=" + str(self.i)
        # print('#' * 40)
        # print(next)
        # print('#' * 40)
        # "36879"
        self.i += 1
        if self.i > 1:
            return
        else:
            yield scrapy.Request(next,callback=self.parse, dont_filter=True )

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.xpath("//div[@class='gallery-top-box']//img/@src").get()
        era = response.meta["era"]

        introduction = response.xpath("//div[@class='cp_blk03_main02_info']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\t","")
        # introduction = introduction.replace("\t","")
        item = GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item
# -*- coding = utf-8 -*-
# @Time : 2021/5/12 10:42
# @Author : waynemars
# @File : mus_1115.py
# @Software : PyCharm
import scrapy
from bs4 import BeautifulSoup
from pip._vendor import requests

from ..items import GgmusItem

class Mus_1115Spider(scrapy.Spider):
    name = 'mus_1115'
    # allowed_domains = ['http://www.automuseum.org.cn/']
    start_urls = ['http://www.automuseum.org.cn/ZLJS/CPJX/list-cpjx1.html?/ZLJS/CSZL/']
    base_url = "http://www.automuseum.org.cn/"

    i = 1
    mus_name_num = '北京汽车博物馆'
    id_num = 1
    mus_ida = 1115
    next_url = []

    def parse(self, response):
        name = response.xpath("//div[@class='cpjx-wk']"
                              "//td[@height='36']//strong/text()").getall()
        name = "".join(name).strip()
        name = name.replace("\t","")
        image = response.xpath("//td[@height='335']//img/@src").get()
        image = self.base_url + image
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        era = ""
        introduction = response.xpath("//td[@class='wz STYLE1']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\r", "")
        introduction = introduction.replace("\n", "")

        # print('#' * 40)
        # print(name)
        # print(image)

        self.i += 1
        next = self.base_url + "ZLJS/CPJX/list-cpjx"+ str(self.i)+ ".html?/ZLJS/CPJX/"
        # # print('#' * 40)
        # # print(next)
        # # print('#' * 40)
        # # "36879"

        # print(self.i)
        # print('#' * 40)
        item = GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        if self.i > 19:
            return
        else:
            yield item
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
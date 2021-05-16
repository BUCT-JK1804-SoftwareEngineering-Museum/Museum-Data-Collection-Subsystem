# -*- coding = utf-8 -*-
# @Time : 2021/5/12 21:23
# @Author : waynemars
# @File : mus_1204.py
# @Software : PyCharm
import scrapy
from bs4 import BeautifulSoup
from pip._vendor import requests

from ..items import GgmusItem

class Mus_1204Spider(scrapy.Spider):
    name = 'mus_1204'
    # allowed_domains = ['http://www.pjcmm.com/']
    start_urls = ['http://www.pjcmm.com/listPro.aspx?cateid=82']
    base_url = "http://www.pjcmm.com/"

    i = 1
    mus_name_num = '平津战役纪念馆'
    id_num = 1
    mus_ida = 1204
    next_url = []

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='listPro']/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            # name = qtq.xpath(".//p/text()").get()
            ima = qtq.xpath(".//img/@src").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+fur,
                                 callback=self.parse_detail, dont_filter=True,
                                 meta = {"image":ima} )

        # 设置“下一页”
        self.i += 1
        next_url = "http://www.pjcmm.com/listPro.aspx?cateid=82&page=" + str(self.i)
        # 测试网络跳转情况

        # print('#' * 40)
        # print(next_url)
        # print(self.i)
        # print('#' * 40)
        if self.i > 3:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        name = response.xpath("//div[@class='contentTitle']/text()").get()
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        era = ""
        introduction = response.xpath("//div[@class='right fr']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\xa0", "")
        introduction = introduction.replace("\r", "")
        item =GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item


    #
    # def parse_detail(self, response):
    #     name = response.meta["name"]
    #     id = str(self.id_num + self.mus_ida * 100000 + 10000)
    #     mus_id = str(self.mus_ida)
    #     mus_name = self.mus_name_num
    #
    #     image = response.xpath("//div[@class='gallery-top-box']//img/@src").get()
    #     era = ""
    #
    #     introduction = response.xpath("//div[@class='cp_blk03_main02_info']//text()").getall()
    #     introduction = "".join(introduction).strip()
    #     introduction = introduction.replace("\t","")
    #     # introduction = introduction.replace("\t","")
    #     item = GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
    #                      introduction=introduction)
    #     self.id_num += 1
    #     yield item
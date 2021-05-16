# -*- coding = utf-8 -*-
# @Time : 2021/5/12 20:53
# @Author : waynemars
# @File : mus_2110.py
# @Software : PyCharm
import scrapy
from bs4 import BeautifulSoup
from pip._vendor import requests

from ..items import GgmusItem

class Mus_2110Spider(scrapy.Spider):
    name = 'mus_2110'
    # allowed_domains = ['http://www.dlnm.org.cn/']
    start_urls = ['http://www.dlnm.org.cn/?_f=boutique']
    base_url = "http://www.dlnm.org.cn/"

    i = 1
    mus_name_num = '大连自然博物馆'
    id_num = 1
    mus_ida = 2110
    next_url = []

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='themelist']/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            name = qtq.xpath(".//p/text()").get()
            ima = qtq.xpath(".//img/@src").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+fur,
                                 callback=self.parse_detail, dont_filter=True,
                                 meta = {"name":name, "image":ima} )

        # 设置“下一页”
        self.i += 1
        next_url = "http://www.dlnm.org.cn/?_f=boutique&p=" + str(self.i)
        # 测试网络跳转情况

        # print('#' * 40)
        # print(next_url)
        # print(self.i)
        # print('#' * 40)
        if self.i > 4:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        # image = self.base_url + image
        era = ""
        introduction = response.xpath("//div[@class='abtxtbox']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\xa0", "")
        introduction = introduction.replace("\r", "")
        item =GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item
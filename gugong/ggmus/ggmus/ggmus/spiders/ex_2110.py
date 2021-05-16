# -*- coding = utf-8 -*-
# @Time : 2021/5/12 21:05
# @Author : waynemars
# @File : ex_2110.py
# @Software : PyCharm
import scrapy
from ..items_ex import GgexItem

class Ex_2110Spider(scrapy.Spider):
    name = 'ex_2110'
    allowed_domains = ['http://www.dlnm.org.cn/']
    start_urls = ['http://www.dlnm.org.cn/?_f=showroom']
    base_url = "http://www.dlnm.org.cn/"

    i = 1
    mus_name_num = '大连自然博物馆'
    id_num = 1
    mus_ida = 2110
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='themelist']/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            fur = qtq.xpath(".//a/@href").get()
            name = qtq.xpath(".//p/text()").get()
            ima = qtq.xpath(".//img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+fur, callback=self.parse_detail,dont_filter=True,
                             meta={"name":name, "image":ima} )

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        time = self.timmme
        info = response.xpath("//div[@class='abtxtbox']//text()").getall()
        info = "".join(info).strip()

        info = info.replace("\n", "")
        info = info.replace("\t", "")
        info = info.replace("\xa0", "")
        info = info.replace("\r", "")
        item = GgexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
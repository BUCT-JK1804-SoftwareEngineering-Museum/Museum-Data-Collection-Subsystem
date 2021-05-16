# -*- coding = utf-8 -*-
# @Time : 2021/5/9 9:52
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
import copy
from ..items_ex import HyexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.hylae.com/']
    start_urls = ['http://www.hylae.com/index.php?ac=article&at=list&tid=33']
    base_url = "http://www.hylae.com/"

    i = 2
    mus_name_num = '汉阳陵博物馆'
    id_num = 1
    mus_ida = 6104

    #找到目录
    def parse(self, response):
        zps = response.xpath("//div[@class='zhanlan-pic']/ul/li")
        for zp in zps:
            name = zp.xpath(".//span[2]/a//text()").get()
            durl = zp.xpath(".//span[1]/a/@href").get()
            ima = zp.xpath(".//span[1]/a/img/@src").get()
            yield scrapy.Request(durl, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name, "image": ima})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        time = ""
        info = response.xpath("//div[@class='list-right-box']//text()").getall()
        info = "".join(info).strip()
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        item =HyexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item

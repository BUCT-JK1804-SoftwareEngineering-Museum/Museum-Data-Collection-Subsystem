# -*- coding = utf-8 -*-
# @Time : 2021/5/7 23:05
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
from ..items_ex import KfexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.kfsbwg.com/']
    start_urls = ['http://www.kfsbwg.com/html/zhanlan/jbcl/']
    base_url = "http://www.kfsbwg.com/"

    mus_name_num = '开封博物馆'
    id_num = 1
    mus_ida = 4105
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='tw']/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            img_url = qtq.xpath(".//div[@class='tw_tu']/a//@href").get()
            ima = qtq.xpath(".//div/a/img/@src").get()
            # print('#' * 40)
            # print(img_url)
            # print(ima)
            # print('#' * 40)
            yield scrapy.Request(img_url, callback=self.parse_detail,dont_filter=True,
                             meta={"image":ima} )

    def parse_detail(self,response):
        name=response.xpath("//h4[@class='show_b']//text()").get()
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        time = self.timmme
        info = response.xpath("//div[@class='show']//text()").getall()
        info = "".join(info).strip()
        item = KfexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
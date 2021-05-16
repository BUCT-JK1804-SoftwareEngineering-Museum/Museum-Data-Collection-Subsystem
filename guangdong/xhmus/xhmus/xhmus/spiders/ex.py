# -*- coding = utf-8 -*-
# @Time : 2021/5/8 10:50
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
from ..item_ex import XhexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['https://www.gznywmuseum.org/']
    start_urls = ['https://www.gznywmuseum.org/zlgg/index.jhtml']
    base_url = "https://www.gznywmuseum.org"

    i = 2
    mus_name_num = '西汉南越王博物馆'
    id_num = 1
    mus_ida = 4402
    timmme = 'null'

    def parse(self, response):
        qtqs = response.xpath("//div[@id='zldtlist']/div")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//div[@class='gg-list-item-title']/span//text()").get()
            img_url = qtq.xpath(".//div[@class='gg-list-item-detail']/a/@href").get()
            ima = qtq.xpath(".//img[@style='width: 200px;height: 150px;']/@src").get()

            if name != None:
                yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,
                                 meta={"name":name, "image":ima} )

        next_url = self.base_url +"/zlgg/index_" + str(self.i) + ".jhtml"
        print('#' * 40)
        print(next_url)
        print('#' * 40)

        self.i += 1
        if self.i > 4:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        time = self.timmme
        info = response.xpath("//div[@class='nbsp-sp-detail-view-middle']//text()").getall()
        info = "".join(info).strip()
        item = XhexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
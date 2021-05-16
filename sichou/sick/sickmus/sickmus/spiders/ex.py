# -*- coding = utf-8 -*-
# @Time : 2021/5/7 18:15
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
from ..items_ex import SickexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['https://www.chinasilkmuseum.com/']
    start_urls = ['https://www.chinasilkmuseum.com/zz/list_17.aspx']
    base_url = "https://www.chinasilkmuseum.com/"

    i = 2
    mus_name_num = '中国丝绸博物馆'
    id_num = 1
    mus_ida = 3303
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//div[@class='show_info']/ul/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//h3[@class='h3']/a//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            ima = qtq.xpath(".//a/img/@src").get()
            ti = qtq.xpath(".//div[@class='show_text']/p[1]//text()").getall()
            ti ="".join(ti).strip()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,
                             meta={"name":name, "image":ima, "time":ti} )

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        time = response.meta["time"]
        info = response.xpath("//div[@class='detail_text']//text()").getall()
        info = "".join(info).strip()
        item = SickexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
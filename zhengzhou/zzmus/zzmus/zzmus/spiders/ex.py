# -*- coding = utf-8 -*-
# @Time : 2021/5/7 17:32
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
from ..items_ex import ZzexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.hnzzmuseum.com/']
    start_urls = ['http://www.hnzzmuseum.com/display9_list.html']
    base_url = "http://www.hnzzmuseum.com/"

    i = 10
    mus_name_num = '郑州博物馆'
    id_num = 1
    mus_ida = 4102
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//div[@class='special_box']/div")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//p[@class='special_t']//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            ima = qtq.xpath(".//img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            if name != None:
                yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,
                                 meta={"name":name, "image":ima} )


        #设置“下一页”
        j = self.i
        next_url = self.base_url+"display"+str(j)+"_list.html"

        #测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        if self.i>11:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        time = self.timmme
        info = response.xpath("//li[@class='n_collection_con_box_c']//text()").getall()
        info = "".join(info).strip()
        item = ZzexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
# -*- coding = utf-8 -*-
# @Time : 2021/5/9 14:55
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy

from ..items_ex import TsexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.nxbwg.com/']
    start_urls = ['http://www.nxbwg.com/c/zlzs.html']
    base_url = "http://www.nxbwg.com/"
    i = 2
    mus_name_num = '宁夏博物馆'
    id_num = 1
    mus_ida = 6402
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//div[@class='article-list']/article")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//h3[@class='article-title']/a//text()").get()
            ima = qtq.xpath(".//div[@class='article-left']/img/@src").get()
            img_url = qtq.xpath(".//h3[@class='article-title']/a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(ima)
            # print(img_url)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,
                             meta={"name":name, "image":ima} )
        # 设置“下一页”
        next_url = self.base_url +"c/zlzs.html" + "?page=" + str(self.i)
        # 测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
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
        # image = self.base_url + image
        time = ""
        info = response.xpath("//div[@class='article-text']//text()").getall()
        info = "".join(info).strip()
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        info = info.replace("\xa0", "")
        item = TsexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
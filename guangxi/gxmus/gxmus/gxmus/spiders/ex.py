# -*- coding = utf-8 -*-
# @Time : 2021/5/8 12:49
# @Author : waynemars
# @File : ex.py
# @Software : PyCharm
import scrapy
from ..items_ex import GxexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.gxmuseum.cn/']
    start_urls = ['http://www.gxmuseum.cn/a/exhibition/index.html']
    base_url = "http://www.gxmuseum.cn/"

    i = 2
    mus_name_num = '广西壮族自治区博物馆'
    id_num = 1
    mus_ida = 4501

    def parse(self, response):
        qtqs = response.xpath("//dl[@class='tbox']/dd/ul/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            fur = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + fur, callback=self.parse_page, dont_filter=True,
                                 meta={"fur": fur})
    def parse_page(self,response):
        zps = response.xpath("//div[@class='listbox']/div")
        for zp in zps:
            name = zp.xpath(".//div[@class='show_sub']/p[1]/a//text()").get()
            durl = zp.xpath(".//div[@class='dp_photo']/a/@href").get()
            ima = zp.xpath(".//div[@class='dp_photo']/a/img/@src").get()
            time = zp.xpath(".//div[@class='show_sub']/p[2]/text()").getall()
            time = "".join(time).strip()
            info = zp.xpath(".//div[@class='show_sub']/p[3]/text()").getall()
            info = "".join(info).strip()

            if name != None:
                yield scrapy.Request(self.base_url + durl, callback=self.parse_detail, dont_filter=True,
                                     meta = {"name":name, "image":ima, "time":time, "info":info} )
        # #
        # 设置“下一页”
        a = response.meta["fur"]
        a = a[:-10]
        # 获得数字编号
        b = response.meta["fur"]
        b = b[10:]
        b = b[4:-11]
        next_url = self.base_url+a+"list_"+b+"_"+str(self.i)+".html"
        # 测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        c = response.xpath("//ul[@class='pagelist']/li[last()-3]//text()").get()
        # print('#' * 40)
        # print(c)
        # print(type(c))
        # print('#' * 40)
        if c==None:
            c = 1
        else:
            c = int(c)
        # print('#' * 40)
        # print(c)
        # print(type(c))
        # print('#' * 40)

        if self.i > c:
            self.i = 2
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse_page, dont_filter=True, meta = {"fur":response.meta["fur"]})

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        time = response.meta["time"]
        info = response.meta["info"]
        item = GxexItem(name=name, id=id, mus_id=mus_id, mus_name=mus_name, image=image,
                           time=time, info=info)
        self.id_num += 1
        yield item
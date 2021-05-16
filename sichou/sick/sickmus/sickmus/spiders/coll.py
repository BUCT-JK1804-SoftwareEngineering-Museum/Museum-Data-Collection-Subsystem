import scrapy
import copy
from ..items import SickmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['https://www.chinasilkmuseum.com/']
    start_urls = ['https://www.chinasilkmuseum.com/zggd/list_21.aspx']
    base_url = "https://www.chinasilkmuseum.com/"

    i = 2
    mus_name_num = '中国丝绸博物馆'
    id_num = 1
    mus_ida = 3303

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//div[@class='about_menu']//li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            if fur != "/list_302.aspx":
                yield scrapy.Request(self.base_url + fur, callback=self.parse_page, dont_filter=True,
                                     meta = {"fur":fur} )

    def parse_page(self,response):

        zps = response.xpath("//div[@class='collect_info']/ul/li")
        for zp in zps:
            name = zp.xpath(".//p/a//text()").get()
            durl = zp.xpath(".//a/@href").get()
            ima = zp.xpath(".//a/img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(durl)
            # print(ima)
            # print('#' * 40)
            # yield scrapy.Request(self.base_url + durl, callback=self.parse_detail, dont_filter=True,
            #                      meta = {"name":name, "image":ima} )

        # 设置“下一页”
        next_url = self.base_url + response.meta["fur"] + "?page=" + str(self.i)
        # 测试网络跳转情况
        self.i += 1
        print('#' * 40)
        print(next_url)
        print('#' * 40)
        if self.i > 127:
            self.i = 2
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse_page, dont_filter=True, meta = {"fur":response.meta["fur"]})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//div[@class='detail_text']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\xa0", "")

        item =SickmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

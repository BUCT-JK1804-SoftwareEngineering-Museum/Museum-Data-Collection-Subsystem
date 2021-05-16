import scrapy
from ..items import KfmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.kfsbwg.com/']
    start_urls = ['http://www.kfsbwg.com/html/wenwu/']
    base_url = "http://www.kfsbwg.com/"

    mus_name_num = '开封博物馆'
    id_num = 1
    mus_ida = 4105

    def parse(self, response):
        qtqs = response.xpath("//div[@id='r_ww']/a")
        for qtq in qtqs:
            fur = qtq.xpath(".//@href").get()
            # print('#' * 40)
            # print(fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + fur, callback=self.parse_page, dont_filter=True,
                                 meta={"fur": fur})

    def parse_page(self, response):
        zps = response.xpath("//ul[@class='tu']/li")
        for zp in zps:
            name = zp.xpath(".//p/a//text()").get()
            durl = zp.xpath(".//a/@href").get()
            ima = zp.xpath(".//a/img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(durl)
            # print(ima)
            # print('#' * 40)
            yield scrapy.Request(durl, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name, "image": ima})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        era = ""
        introduction = ""
        item = KfmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                           introduction=introduction)
        self.id_num += 1
        yield item

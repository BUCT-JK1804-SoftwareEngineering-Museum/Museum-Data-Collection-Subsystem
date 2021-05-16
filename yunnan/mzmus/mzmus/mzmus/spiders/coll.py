import scrapy
from ..items import MzmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.ynnmuseum.com/']
    start_urls = ['http://www.ynnmuseum.com/products_list1/&pageNo_FrontProducts_list01-1345168125420=1&pageSize_FrontProducts_list01-1345168125420=500.html']
    base_url = "http://www.ynnmuseum.com/"

    i = 2
    mus_name_num = '云南民族博物馆'
    id_num = 1
    mus_ida = 5302

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='mainul productlist-02']/li")
        for qtq in qtqs:
            name = qtq.xpath(".//div[@class='pic']/a/@title").get()
            img_url = qtq.xpath(".//div[@class='pic']/a/@href").get()
            ima = qtq.xpath(".//div[@class='pic']/a/img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print(ima)
            # print('#' * 40)
            if name != None:
                yield scrapy.Request(self.base_url + img_url,
                                     callback=self.parse_detail, dont_filter=True,
                                     meta = {"name":name, "image":ima} )

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath(" //div[@class='detail']//text() ").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n","")
        introduction = introduction.replace("\t","")
        item =MzmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

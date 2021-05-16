import scrapy
from ..items import NymusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://nyhhg.com/']
    start_urls = ['http://nyhhg.com/a/xy/list_1.html']
    base_url = "http://nyhhg.com/"

    mus_name_num = '南阳汉画馆'
    id_num = 1
    mus_ida = 4104

    def parse(self, response):
        qtqs = response.xpath("//div[@class='cateslist']/dl/dd")
        # print('#' * 40)
        # print(qtqs)
        # print('#' * 40)
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//div[@class='txt']/a//text()").get()
            img_url = qtq.xpath(".//div[@class='txt']/a//@href").get()
            ima = qtq.xpath(".//div[@class='img']/a/img//@src").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)

            yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,
                                 meta={"name":name, "image":ima} )


    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        era = "null"
        introduction = "null"
        item=NymusItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item
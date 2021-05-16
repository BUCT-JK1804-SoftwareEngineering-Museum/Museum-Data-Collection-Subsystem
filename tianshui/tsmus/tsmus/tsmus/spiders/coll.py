import scrapy
from ..items import TsmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.nxbwg.com/']
    start_urls = ['http://www.nxbwg.com/c/jpww.html']
    base_url = "http://www.nxbwg.com/"
    i = 2
    mus_name_num = '宁夏博物馆'
    id_num = 1
    mus_ida = 6402

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//div[@class='article-list grid']/div")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            name = qtq.xpath(".//h3[@class='article-title jp-pb-title']/a//text()").get()
            ima = qtq.xpath(".//div[@class='img-zoom']/img/@src").get()
            # print('#' * 40)
            # print(fur)
            # print(name)
            # print(ima)
            # print('#' * 40)
            if name!=None:
                yield scrapy.Request(self.base_url+ fur, callback=self.parse_detail, dont_filter=True,
                                     meta = {"name":name, "image":ima} )

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        # image = self.base_url + image
        era = response.xpath("//div[@class='article-text']/p[3]/text()").get()

        introduction = response.xpath("//div[@class='article-text']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\xa0", "")
        item =TsmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item
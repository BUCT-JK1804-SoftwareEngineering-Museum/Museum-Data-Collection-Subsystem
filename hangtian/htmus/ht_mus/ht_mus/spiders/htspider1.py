import scrapy
from ..items import HtMusItem



class Htspider1Spider(scrapy.Spider):
    name = 'htspider1'
    allowed_domains = ['http://www.casc-spacemuseum.com/']
    start_urls = ['http://www.casc-spacemuseum.com/exhibition.aspx']
    base_url = "http://www.casc-spacemuseum.com/"

    id_num = 1
    mus_ida = 1105
    mus_name_num = '中国航天博物馆'
    timmme = '常年开放'

    def parse(self, response):
        zls = response.xpath("//ul[@class='business_list']/li")
        for zl in zls:
            # 爬取名字和图片地址
            # name = zl.xpath(".//div[@class='basicDes']/h3/text()").get()
            name = zl.xpath(".//h3/a/@title").get()
            image_url = zl.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(image_url)
            yield scrapy.Request(self.base_url + image_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name})


    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//div[@style='text-align:center;']/img/@src").get()
        image = self.base_url + image
        time = self.timmme
        info = response.xpath("//div[@class='article']/p/span//text()").getall()
        info = "".join(info).strip()
        item=HtMusItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1
        yield item
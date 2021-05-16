import scrapy
from ..items import BjexItem

class ExspiderSpider(scrapy.Spider):
    name = 'exspider'
    allowed_domains = ['http://www.bjqtm.com']
    start_urls = ['http://www.bjqtm.com/clzl/jbcl/index.html']
    base_url = "http://www.bjqtm.com"

    mus_name_num = '宝鸡青铜器博物馆'
    timmme = '常年开放'

    id_num = 1
    mus_ida = 6108

    def parse(self, response):
        zls = response.xpath("//ul[@class='clearfix']/li")
        for zl in zls:
            # 爬取名字和图片地址
            name = zl.xpath(
                ".//h2[@class='mar-t10 mar-b10 pad-l5 pad-r5 c-333 t-a-c f-siz16 f-wei-b ellipsis']//text()").get()
            img_url = zl.xpath(".//a[@class='pos-a w100 h100 dis-b t l']/@href").get()
            print('#'*40)
            print(type(name))
            print(type(img_url))
            yield scrapy.Request(self.base_url + img_url, callback=self.parse_detail, dont_filter=True, meta={"name": name})


    def parse_detail(self,response):
        exh_name = response.meta["name"]
        exh_id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        exh_picture = response.xpath("//img/@src").get()
        exh_picture = self.base_url + exh_picture
        exh_time = self.timmme
        exh_info = response.xpath("//div[@class='mar-t20 pad-b25 article']/p[2]//text()").getall()
        exh_info = "".join(exh_info).strip()
        item=BjexItem(exh_name=exh_name,exh_id=exh_id,mus_id=mus_id,mus_name=mus_name,exh_picture=exh_picture,
                      exh_time=exh_time,exh_info=exh_info)
        self.id_num += 1

        yield item
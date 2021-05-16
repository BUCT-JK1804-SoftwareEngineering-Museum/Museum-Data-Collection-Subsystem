import scrapy
from ..items import JunboexItem


class Jbexspider1Spider(scrapy.Spider):
    name = 'jbexspider1'
    allowed_domains = ['www.jb.mil.cn/']
    start_urls = ['http://www.jb.mil.cn/zlcl/jbcl/']
    base_url = "http://www.jb.mil.cn/zlcl/jbcl/"
    id_num = 1
    mus_ida = 1104
    mus_name_num = '中国人民革命军事博物馆'
    timmme = '常年开放'

    def parse(self, response):
        zls = response.xpath("//div[@class='basicList']/ul/li")
        for zl in zls:
            # 爬取名字和图片地址
            # name = zl.xpath(".//div[@class='basicDes']/h3/text()").get()
            name = zl.xpath(".//h3/text()").get()
            image = zl.xpath(".//img/@src").get()
            intro_url = zl.xpath(".//dt/a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(intro_url)
            yield scrapy.Request(self.base_url + intro_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name, "image": image})


    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = self.base_url + response.meta["image"]
        time = self.timmme
        info = response.xpath("//div[@class='TRS_Editor']/p[1]//text()").getall()
        info = "".join(info).strip()
        item=JunboexItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1

        yield item
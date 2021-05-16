import scrapy
from ..exitems import CyexItem

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['http://www.cyjng.net/']
    start_urls = ['http://www.cyjng.net/Default.aspx?tabid=261&language=zh-CN']
    base_url = "http://www.cyjng.net/"

    id_num = 1
    mus_ida = 3105
    mus_name_num = '陈云纪念馆'
    timmme = '常年开放'

    def parse(self, response):
        zls = response.xpath("//div[@class='leftmenu']/a")
        # print('#' * 40)
        # print(zls)
        # print('#' * 40)
        for zl in zls:
            name = zl.xpath(".//h3/text()").get()
            intro_url = zl.xpath(".//@href").get()
            print('#' * 40)
            print(name)
            # print(intro_url)
            print('#' * 40)
            yield scrapy.Request(self.base_url + intro_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name})


    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//img[@width='650' and @height='433']/@src").get()
        image = self.base_url + image
        time = self.timmme
        info = response.xpath("//div[@class='c_content']//text()").getall()
        info = "".join(info).strip()
        item=CyexItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1

        yield item
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'zyhymus'
    allowed_domains = ['http://www.zunyihy.cn/']
    start_urls = ['http://www.zunyihy.cn/searchs/collection.html?0.17377033055156654&category_id=&tpl_file=collection&content=&pagesize=9&sort=&p=1']
    base_domain = "http://www.zunyihy.cn"
    col_id_num: int=520110001
    mus_id_num: int=5201
    mus_name_num='遵义会议博物馆'

    def parse(self, response):
        #SelectorList对象

        duanzidivs = response.xpath("//div[@class='list_wenchuang']/div")
        print('#' * 40)
        print(duanzidivs)
        print('#' * 40)
        for duanzidiv in duanzidivs:
            #Selector对象
            name = duanzidiv.xpath(".//div[@class='t4 ellipsis']//text()").get()
            image = duanzidiv.xpath(".//div[@class='img']/img/@src").get()
            image = self.base_domain + image
            img_url = duanzidiv.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_domain + img_url, callback=self.parse_detail, dont_filter=True,meta={"name": name, "image": image})
        next_url = response.xpath("//ul[@class='page-box p-show clear']/li[@class='page-item next']/a/@href").get()
        if not next_url:

            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        col_name = response.meta["name"]
        col_picture = response.meta["image"]
        introduction = response.xpath("//div[@class='situation_1']//text()").getall()
        introduction = "".join(introduction).strip()
        col_info=str(introduction).replace("\r","").replace("\n","").replace("\xa0","").replace("\t","")
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era="遵义会议",
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
import scrapy

from ..items import QsbkexItem

class JsyzmusexSpider(scrapy.Spider):
    name = 'jsyzmusex'
    allowed_domains = ['http://www.jinshasitemuseum.com']
    start_urls = ['http://www.jinshasitemuseum.com/Exhibition/ExhibitionBasicDisplay']
    exh_id_num: int=510710001
    mus_id_num: int=5107
    mus_name_num='成都金沙遗址博物馆'

    def parse(self, response):
        ex_1s=response.xpath("//div[@class='display-warp lg']/div[@class='container-fluid']/div")
        for ex_1 in ex_1s:
            exh_name=ex_1.xpath(".//dd/text()").get()
            exh_picture=ex_1.xpath(".//img/@src").get()
            info_url=ex_1.xpath(".//a/@href").get()
            info_url="http://www.jinshasitemuseum.com"+str(info_url)
            # print(info_url)
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"exh_name":exh_name,"exh_picture":exh_picture})
        ex_2s=response.xpath("//div[@class='w']//div[@class='mt cultural-warp']/div")
        for ex_2 in ex_2s:
            exh_name=ex_2.xpath(".//div[@class='title']/text()").get()
            exh_name=str(exh_name).replace(" ", "").replace("\n","").replace("\r","")
            exh_picture=ex_2.xpath(".//dt/img/@src").get()
            exh_time='文化景观'
            exh_info=ex_2.xpath(".//dd//div[@class='cultural-content']//text()").getall()
            exh_info="".join(exh_info).strip().replace("\n","").replace("\r","").replace("\xa0","")
            # print('#' * 40 + '1')
            # print(exh_name)
            # print(exh_picture)
            # print(exh_time)
            # print(exh_info)
            # print('#' * 40 + '2')
            item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num,
                              mus_name=self.mus_name_num,
                              exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
            self.exh_id_num += 1
            yield item
        pass
    def parse_info(self,response):
        exh_name=response.meta['exh_name']
        exh_picture=response.meta['exh_picture']
        exh_time='常设展览'
        exh_info=response.xpath("//div[@class='museum-text']//span//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_info=str(exh_info).replace("\n","").replace("\r","").replace("\xa0","")
        # print('#' * 40 + '1')
        # print(exh_name)
        # print(exh_picture)
        # print(exh_time)
        # print(exh_info)
        # print('#' * 40 + '2')
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
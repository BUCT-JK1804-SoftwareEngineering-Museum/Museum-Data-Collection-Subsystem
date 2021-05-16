import scrapy

from ..items import QsbkexItem

class GssmusexSpider(scrapy.Spider):
    name = 'gssmusex'
    allowed_domains = ['http://www.gansumuseum.com']
    start_urls = ['http://www.gansumuseum.com/zl/list-0-1.html']
    exh_id_num: int=620110001
    mus_id_num: int=6201
    mus_name_num='甘肃省博物馆'

    def parse(self, response):
        for i in range (1,11):#11
            page_url="http://www.gansumuseum.com/zl/list-0-"+str(i)+".html"
            # print('#' * 40 + '1')
            # print(page_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        gsexdivs=response.xpath("//div[@class='play_list']/ul/li")
        for gsexdiv in gsexdivs:
            exh_name=gsexdiv.xpath(".//div[@class='title']/label/text()").get()
            exh_picture="http://www.gansumuseum.com"+gsexdiv.xpath(".//a/img/@src").get()
            info_url="http://www.gansumuseum.com"+gsexdiv.xpath(".//div[@class='foot']/a[last()]/@href").get()
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"exh_name":exh_name,"exh_picture":exh_picture})
        pass
    def parse_info(self,response):
        exh_name=response.meta['exh_name']
        exh_picture=response.meta['exh_picture']
        exh_info=response.xpath("//div[@class='inner']//text()").getall()
        exh_info="".join(exh_info).strip().replace("\n","").replace("\xa0","")
        if not exh_info:
            exh_info='无'
        exh_time='临时展览'
        # print('#' * 40 + '1')
        # print(exh_name)
        # print(exh_picture)
        # print(exh_info)
        # print(exh_time)
        # print('#' * 40 + '2')
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
        pass
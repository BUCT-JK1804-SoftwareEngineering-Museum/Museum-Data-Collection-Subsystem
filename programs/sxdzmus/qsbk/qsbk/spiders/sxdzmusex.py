import scrapy

from ..items import QsbkexItem

class SxdzmusSpider(scrapy.Spider):
    name = 'sxdzmusex'
    allowed_domains = ['http://www.sxgm.org']
    start_urls = ['http://www.sxgm.org/home/picnews/index/c_id/94/lanmu/59.html']
    exh_id_num: int = 141010001
    mus_id_num: int = 1410
    mus_name_num = '山西地质博物馆'

    def parse(self, response):
        for i in range(94,96,1):
            page_url="http://www.sxgm.org/home/picnews/index/c_id/"+str(i)+"/lanmu/59.html"
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        sxdivs=response.xpath("//div[@class='center_right']//ul[@class='page_picnew_list']/li")
        for sxdiv in sxdivs:
            col_name=sxdiv.xpath(".//img/@title").get()
            col_picture=sxdiv.xpath(".//img/@src").get()
            col_picture="http://www.sxgm.org"+col_picture
            info_url=sxdiv.xpath(".//a/@href").get()
            info_url="http://www.sxgm.org"+info_url
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(info_url, callback=self.parse_info, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture})

    def parse_info(self, response):
        exh_name = response.meta['col_name']
        exh_picture = response.meta['col_picture']
        exh_info=response.xpath("//div[@class=' new_content_view']//text()").getall()
        exh_info="".join(exh_info).strip().replace("\n","").replace("\xa0","")
        if not exh_info:
            exh_info='无'
        exh_time='常设展览'
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
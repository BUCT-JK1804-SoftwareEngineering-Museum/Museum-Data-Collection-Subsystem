import scrapy

from ..items import QsbkItem

class SxdzmusSpider(scrapy.Spider):
    name = 'sxdzmus'
    allowed_domains = ['http://www.sxgm.org']
    start_urls = ['http://www.sxgm.org/home/picnews/index/c_id/104/lanmu/61.html']
    col_id_num: int = 141010001
    mus_id_num: int = 1410
    mus_name_num = '山西地质博物馆'

    def parse(self, response):
        for i in range(104,109,1):
            page_url="http://www.sxgm.org/home/picnews/index/c_id/"+str(i)+"/lanmu/61.html"
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
        col_name = response.meta['col_name']
        col_picture = response.meta['col_picture']
        col_info=response.xpath("//div[@class=' new_content_view']//text()").getall()
        col_info="".join(col_info).strip().replace("\n","")
        if not col_info:
            col_info='无'
        col_era='现代'
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
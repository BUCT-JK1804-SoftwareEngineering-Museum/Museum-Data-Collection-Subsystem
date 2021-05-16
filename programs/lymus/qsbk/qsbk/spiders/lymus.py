import scrapy

from ..items import QsbkItem

class LymusSpider(scrapy.Spider):
    name = 'lymus'
    allowed_domains = ['http://www.lymuseum.com']
    start_urls = ['http://www.lymuseum.com/list.php?fid=47']
    base_next_page="http://www.lymuseum.com/"
    col_id_num :int = 410310001
    mus_id_num :int =4103
    mus_name_num='洛阳博物馆'

    def parse(self, response):
        pagedivs=response.xpath("//div[@class='list_title']//td")
        for pagediv in pagedivs:
            next_page=pagediv.xpath(".//div/a/@href").get()
            next_page=self.base_next_page+str(next_page)
            # print('#' * 40 + '1')
            # print(next_page)
            # print('#' * 40 + '2')
            yield scrapy.Request(next_page,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        lydivs=response.xpath("//div[@class='Main']//td[@class='middle']/table//div")
        for lydiv in lydivs:
            col_name=lydiv.xpath(".//a/@title").get()
            col_picture=lydiv.xpath(".//img/@src").get()
            info_url=lydiv.xpath(".//a/@href").get()
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(self.base_next_page+str(info_url))
            # print('#' * 40 + '2')
            yield scrapy.Request(self.base_next_page+str(info_url),callback=self.parse_info,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='Main']//td[@class='middle']//table[1]//td//span//text()").getall()
        col_info="".join(col_info).strip()
        col_info=str(col_info).replace(" ","").replace("\xa0","")
        col_era=response.xpath("//div[@class='Main']//td[@class='middle']//table[1]//td//span[1]//text()").get()
        col_era = str(col_era).replace(" ", "").replace("\xa0", "")
        if not col_info:
            col_info='无'
            col_era='不详'
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_info)
        # print(col_era)
        # print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
        pass
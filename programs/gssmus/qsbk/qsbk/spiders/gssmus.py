import scrapy

from ..items import QsbkItem

class GssmusSpider(scrapy.Spider):
    name = 'gssmus'
    allowed_domains = ['http://www.gansumuseum.com']
    start_urls = ['http://www.gansumuseum.com/dc/list-58-1.html']
    col_id_num: int=620110001
    mus_id_num: int=6201
    mus_name_num='甘肃省博物馆'

    def parse(self, response):
        for i in range (1,98):#98
            page_url="http://www.gansumuseum.com/dc/list-58-"+str(i)+".html"
            # print('#' * 40 + '1')
            # print(page_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        gsdivs=response.xpath("//div[@class='play_list']/ul/li")
        for gsdiv in gsdivs:
            col_name=gsdiv.xpath(".//div[@class='title']/label/text()").get()
            col_picture=gsdiv.xpath(".//img[@class='bg pull-left']/@src").get()
            col_picture="http://www.gansumuseum.com"+str(col_picture)
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print('#' * 40 + '2')
            info_url=gsdiv.xpath(".//div[@class='foot']//a[last()]/@href").get()
            info_url="http://www.gansumuseum.com"+info_url
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='inner']//p//text()").getall()
        col_info="".join(col_info).strip().replace("\n","").replace("\xa0","").replace(" ","")
        col_era='见介绍'
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_info)
        # print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
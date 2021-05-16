import scrapy

from ..items import QsbkItem

class ZgcymusSpider(scrapy.Spider):
    name = 'zgcymus'
    allowed_domains = ['http://www.teamuseum.cn']
    start_urls = ['http://www.teamuseum.cn/news/holding.htm?newsType=5']
    col_id_num: int = 331010001
    mus_id_num: int = 3310
    mus_name_num = '中国茶叶博物馆'

    def parse(self, response):
        for i in range(5,11):#11
            page_url="http://www.teamuseum.cn/news/holding.htm?newsType="+str(i)
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        col_era=response.xpath("//div[@class='pro_tab']//li[@class='active']/a/text()").get()
        zgcydivs=response.xpath("//div[@class='zyz_box adContainer zyz_fc_box']//li")
        for zgcydiv in zgcydivs:
            col_name=zgcydiv.xpath(".//a/h2/text()").get()
            col_picture=zgcydiv.xpath(".//img/@src").get()
            info_url=zgcydiv.xpath(".//a/@href").get()
            info_url="http://www.teamuseum.cn"+info_url
            yield scrapy.Request(info_url, callback=self.parse_info, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture,"col_era":col_era})

    def parse_info(self, response):
        col_name = response.meta['col_name']
        col_name=str(col_name)
        col_picture = response.meta['col_picture']
        col_info=response.xpath(".//div[@class='pro_detail']//text()").getall()
        col_info="".join(col_info).strip().replace("\n","").replace("\xa0","").replace("\r","").replace("\t","")
        if not col_info:
            col_info='无'
        col_era=response.meta['col_era']
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
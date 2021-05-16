import scrapy

from ..items import QsbkexItem

class ZgcymusSpider(scrapy.Spider):
    name = 'zgcymusex'
    allowed_domains = ['http://www.teamuseum.cn']
    start_urls = ['http://www.teamuseum.cn/information/temp_information_list.htm']
    exh_id_num: int = 331010001
    mus_id_num: int = 3310
    mus_name_num = '中国茶叶博物馆'

    def parse(self, response):
        page_url="http://www.teamuseum.cn/information/temp_information_list.htm"
        yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        zgcydivs=response.xpath("//div[@class='right']//li")
        for zgcydiv in zgcydivs:
            col_name=zgcydiv.xpath(".//div[@class='linshi_cnt']/h2/text()").get()
            col_era = response.xpath("//div[@class='linshi_cnt']//div/text()[1]").get()
            col_picture=zgcydiv.xpath(".//img/@src").get()
            info_url=zgcydiv.xpath(".//a/@href").get()
            info_url="http://www.teamuseum.cn"+info_url
            yield scrapy.Request(info_url, callback=self.parse_info, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture,"col_era":col_era})

    def parse_info(self, response):
        exh_name = response.meta['col_name']
        exh_name=str(exh_name)
        exh_picture = response.meta['col_picture']
        exh_info=response.xpath(".//div[@class='kp_dl_cnt']//text()").getall()
        exh_info="".join(exh_info).strip().replace("\n","").replace("\xa0","").replace("\r","").replace("\t","")
        if not exh_info:
            exh_info='无'
        exh_time=response.meta['col_era']
        exh_time='临时展览'
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
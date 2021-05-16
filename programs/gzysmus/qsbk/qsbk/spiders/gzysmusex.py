import scrapy

from ..items import QsbkexItem
class GzysmusSpider(scrapy.Spider):
    name = 'gzysmusex'
    allowed_domains = ['https://www.gzam.com.cn']
    start_urls = ['https://www.gzam.com.cn/cp/list_24.aspx?lcid=3&page=1']
    exh_id_num: int = 440810001
    mus_id_num: int = 4408
    mus_name_num = '广州艺术博物院'

    def parse(self, response):
        page_url="https://www.gzam.com.cn/zzzc/list_18.aspx?State=0"
        yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        gzdivs=response.xpath("//div[@class='Content']//ul[@class='ul']/li")
        for gzdiv in gzdivs:
            col_name=gzdiv.xpath(".//img/@alt").get()
            col_picture=gzdiv.xpath(".//img/@src").get()
            col_picture="https://www.gzam.com.cn"+col_picture
            info_url=gzdiv.xpath('.//a/@href').get()
            info_url="https://www.gzam.com.cn"+info_url
            yield scrapy.Request(info_url, callback=self.parse_info, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture})

    def parse_info(self, response):
        exh_name = response.meta['col_name']
        exh_name=str(exh_name)
        exh_picture = response.meta['col_picture']
        #col_name=response.xpath(".//div[@class='yc_infoCon']//p[contains(string(),col_name)]//text()").get()
        exh_info=response.xpath(".//div[@class='info_txt']//text()").getall()
        exh_info="".join(exh_info).strip().replace("\n","").replace("\xa0","").replace("\r","").replace("\t","")
        if not exh_info:
            exh_info='无'
        exh_time='常设展览'
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
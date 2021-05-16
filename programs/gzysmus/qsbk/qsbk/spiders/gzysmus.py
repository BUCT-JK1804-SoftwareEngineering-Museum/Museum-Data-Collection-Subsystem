import scrapy

from ..items import QsbkItem
class GzysmusSpider(scrapy.Spider):
    name = 'gzysmus'
    allowed_domains = ['https://www.gzam.com.cn']
    start_urls = ['https://www.gzam.com.cn/cp/list_24.aspx?lcid=3&page=1']
    col_id_num: int = 440810001
    mus_id_num: int = 4408
    mus_name_num = '广州艺术博物院'

    def parse(self, response):
        for i in range(1,49):#49
            page_url="https://www.gzam.com.cn/cp/list_24.aspx?lcid=3&page="+str(i)
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        gzdivs=response.xpath("//div[@class='Content']//dl[@class='dl']/dd")
        for gzdiv in gzdivs:
            col_name=gzdiv.xpath(".//p[@class='title']/text()").get()
            col_picture=gzdiv.xpath(".//img/@src").get()
            col_picture="https://www.gzam.com.cn"+col_picture
            info_url=gzdiv.xpath('.//a/@href').get()
            info_url="https://www.gzam.com.cn"+info_url
            yield scrapy.Request(info_url, callback=self.parse_info, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture})

    def parse_info(self, response):
        col_name = response.meta['col_name']
        col_name=str(col_name)
        col_picture = response.meta['col_picture']
        #col_name=response.xpath(".//div[@class='yc_infoCon']//p[contains(string(),col_name)]//text()").get()
        col_info=response.xpath(".//div[@class='yc_infoCon']//text()").getall()
        col_info="".join(col_info).strip().replace("\n","").replace("\xa0","").replace("\r","").replace("\t","")
        if not col_info:
            col_info='无'
        col_era='见名称'
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkexItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'ncbyqymusex'
    allowed_domains = ['http://www.81-china.com']
    start_urls = ['http://www.81-china.com/zhanlan/111.html']
    base_next_page = "http://www.81-china.com"
    exh_id_num: int = 360410008
    mus_id_num: int = 3604
    mus_name_num = '南昌八一起义纪念馆'
    exh_time_num='常设展览'
    def parse(self, response):
        musdivs=response.xpath("//div[@class='list_content']/ul[@class='list_ul']/li")
        for musdiv in musdivs:
            exh_name=musdiv.xpath(".//div[@class='right_listcon']/h3/a/text()").get()
            exh_picture=musdiv.xpath(".//div[@class='left_listcon']/a/@href").get()
            exh_picture=self.base_next_page+exh_picture
            info_url = musdiv.xpath(".//div[@class='right_listcon']/h3/a/@href").get()
            yield scrapy.Request(self.base_next_page+str(info_url),callback=self.parse_info,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture})
        pass
    def parse_info(self,response):
        exh_name=response.meta['exh_name']
        exh_picture=response.meta['exh_picture']
        exh_info=response.xpath("//div[@class='detial_txt']//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_info=str(exh_info).replace("\n","").replace("\r","").replace("\xa0","").replace("\t","").replace(" ","").replace("\u2003","").replace("'","")
        if not exh_info:
            exh_info='无'
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num, exh_picture=exh_picture,
                          exh_time=self.exh_time_num, exh_info=exh_info)
        self.exh_id_num+=1
        yield item
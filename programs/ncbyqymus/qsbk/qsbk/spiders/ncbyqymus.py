import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'ncbyqymus'
    allowed_domains = ['http://www.81-china.com']
    start_urls = ['http://www.81-china.com/collect/60/1.html']
    base_next_page = "http://www.81-china.com"
    col_id_num: int = 360410001
    mus_id_num: int = 3604
    mus_name_num = '南昌八一起义纪念馆'
    col_era_num='八一记忆'
    def parse(self, response):
        musdivs=response.xpath("//div[@class='list_content']/ul[@class='list_ul']/li")
        for musdiv in musdivs:
            col_name=musdiv.xpath(".//div[@class='right_listcon']/h3/a/text()").get()
            col_picture=musdiv.xpath(".//div[@class='left_listcon']/a/@href").get()
            col_picture=self.base_next_page+col_picture
            info_url = musdiv.xpath(".//div[@class='right_listcon']/h3/a/@href").get()
            yield scrapy.Request(self.base_next_page+str(info_url),callback=self.parse_info,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})
        now_page = response.xpath("//div[@class='flickr']/span[@class='current']/text()").get()
        if int(now_page)>=18:
            return
        else:
            next_page=response.xpath("//div[@class='flickr']/a[last()]/@href").get()
            # print('#' * 40 + '1')
            # print(self.base_next_page + str(next_page))
            # print('#' * 40 + '2')
            yield scrapy.Request(self.base_next_page+str(next_page),callback=self.parse,dont_filter=True)
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='detial_txt']//text()").getall()
        col_info="".join(col_info).strip()
        col_info=str(col_info).replace("\n","").replace("\r","").replace("\xa0","").replace("\t","").replace(" ","")
        if not col_info:
            col_info='无'
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=self.col_era_num,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
        pass
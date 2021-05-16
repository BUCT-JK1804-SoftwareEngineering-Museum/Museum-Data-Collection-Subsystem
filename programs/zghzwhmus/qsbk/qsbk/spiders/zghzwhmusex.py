import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkexItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'zghzwhmusex'
    allowed_domains = ['http://www.hzwhbwg.com']
    start_urls = ['http://www.hzwhbwg.com/index.php/list-11-1.html']
    base_url="http://www.hzwhbwg.com"
    exh_id_num: int = 340210001
    mus_id_num: int = 3402
    mus_name_num = '中国徽州文化博物馆'
    def parse(self, response):
        zghzwhdivs=response.xpath("//div[@class='exhibition']/ul/li")
        for zghzwhdiv in zghzwhdivs:
            exh_name=zghzwhdiv.xpath(".//div[@class='exhmain']/h5/text()").get()
            exh_name=str(exh_name).replace("\r","").replace("\n","")
            exh_picture=zghzwhdiv.xpath(".//div[@class='exhimg']/img/@src").get()
            exh_picture=self.base_url+str(exh_picture)
            print('#' * 40 + '1')
            print(exh_picture)
            print('#' * 40 + '2')
            exh_info=zghzwhdiv.xpath(".//div[@class='exhmain']/p/text()").get().strip()
            exh_time='常设展览'
            item = QsbkexItem(exh_id=self.exh_id_num,exh_name=exh_name,mus_id=self.mus_id_num,mus_name=self.mus_name_num,
                              exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
            self.exh_id_num += 1
            yield item
        pass

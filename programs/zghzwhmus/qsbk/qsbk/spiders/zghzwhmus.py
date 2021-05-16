import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'zghzwhmus'
    allowed_domains = ['http://www.hzwhbwg.com']
    start_urls = ['http://www.hzwhbwg.com/index.php/list-3.html']
    base_next_page = "http://www.hzwhbwg.com"
    col_id_num: int = 340210001
    mus_id_num: int = 3402
    mus_name_num = '中国徽州文化博物馆'
    col_era_num='不详'
    def parse(self, response):
        zghzwhdivs=response.xpath("//div[@class='product']/ul/li")
        for zghzwhdiv in zghzwhdivs:
            col_name='仅有图片 名字无'
            col_picture=zghzwhdiv.xpath(".//a/img/@src").get()
            col_picture=self.base_next_page+col_picture
            print('#' * 40 + '1')
            print(col_picture)
            print('#' * 40 + '2')
            col_info='无'
            item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=self.col_era_num,
                            col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
            self.col_id_num += 1
            yield item
        now_page = response.xpath("//div[@class='product']/p[@class='k_pagelist']/strong/text()").get()
        if int(now_page)>=5:
            return
        else:
            next_page=response.xpath("//div[@class='product']/p[@class='k_pagelist']/a[last()]/@href").get()
            # print('#' * 40 + '1')
            # print(self.base_next_page + str(next_page))
            # print('#' * 40 + '2')
            yield scrapy.Request(self.base_next_page+str(next_page),callback=self.parse,dont_filter=True)
        pass

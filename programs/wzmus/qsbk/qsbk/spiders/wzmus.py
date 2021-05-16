import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'wzmus'
    allowed_domains = ['http://www.wzmuseum.cn']
    start_urls = ['http://www.wzmuseum.cn/Col/Col5/Index_1.aspx']
    base_next_page = "http://www.wzmuseum.cn"
    col_id_num: int = 330610001
    mus_id_num: int = 3306
    mus_name_num = '温州博物馆'
    col_era_num='见名字'
    def parse(self, response):
        wzdivs=response.xpath("//div[@class='jpresult']/ul[@class='jpul']/li")
        for wzdiv in wzdivs:
            col_name=wzdiv.xpath(".//a/span//text()").get().strip()
            col_picture = wzdiv.xpath(".//a/img/@src").get()
            col_picture = self.base_next_page+str(col_picture)
            info_url = wzdiv.xpath(".//a/@href").get()
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(str(info_url),callback=self.parse_detail,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
        now_page = response.xpath("//div[@class='NewsPage']/font/text()").get().strip()
        now_page_int:int = int(now_page)
        if now_page_int >= 6:
            return
        else:
            next_page=response.xpath("//div[@class='NewsPage']/a[last()-1]/@href").get()
            print('#'*40 + '1' )
            print(self.base_next_page + str(next_page))
            print('#' * 40 + '2')
            yield scrapy.Request(self.base_next_page + str(next_page),callback=self.parse,dont_filter=True)
        pass
    def parse_detail(self, response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='newstxt']//text()").getall()
        col_info="".join(col_info).strip()
        col_info=str(col_info).replace(" ","").replace("'","")
        if not col_info:
            col_info='无'
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_info)
        # print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=self.col_era_num,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
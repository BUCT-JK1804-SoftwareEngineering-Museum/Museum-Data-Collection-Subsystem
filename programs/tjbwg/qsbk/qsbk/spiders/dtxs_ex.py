import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import DtxsexItem
#from fake_useragent import UserAgent
#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'dtxs_ex'
    allowed_domains = ['http://www.dtxsmuseum.com/']
    start_urls = ['http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=27&page=1']
    base_domain = "http://www.dtxsmuseum.com"
    exh_id_num: int=610910001
    mus_id_num: int=6109
    mus_name_num='大唐西市博物馆'
    def parse(self, response):
        #SelectorList对象
        duanzidivs = response.xpath("//div[@class='news-pic-list']/ul[@class='clearfix']/li")
        for duanzidiv in duanzidivs:
            #Selector对象
            exh_id = self.exh_id_num
            self.exh_id_num+=1
            mus_id=self.mus_id_num
            mus_name=self.mus_name_num
            exh_name = duanzidiv.xpath(".//span[@class='title']//text()").get()
            exh_picture = duanzidiv.xpath(".//span[@class='pic thumbnail']/img/@src").get()
            exh_picture = self.base_domain + exh_picture
            img_url = duanzidiv.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_domain + img_url, callback=self.parse_detail, dont_filter=True,meta={"exh_id":exh_id,"exh_name":exh_name,"mus_id":mus_id,"mus_name":mus_name,"exh_picture":exh_picture})
        next_url = response.xpath("//div[@class='digg clearfix']/a[last()]/@href").get()
        current = response.xpath("//div[@class='digg clearfix']/span[@class='current']//text()").get()
        int_current=int(current)
        if int_current >= 2:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        exh_id = response.meta["exh_id"]
        exh_name=response.meta["exh_name"]
        mus_id=response.meta["mus_id"]
        mus_name=response.meta["mus_name"]
        exh_picture = response.meta["exh_picture"]
        exh_time=response.xpath("//div[@id='div_news_date']//text()").get()
        exh_info = response.xpath("//div[@class='news-content']//text()").getall()
        print('*' * 40)
        print(exh_time)
        print('*' * 40)
        exh_info = "".join(exh_info).strip()
        item = DtxsexItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        yield item
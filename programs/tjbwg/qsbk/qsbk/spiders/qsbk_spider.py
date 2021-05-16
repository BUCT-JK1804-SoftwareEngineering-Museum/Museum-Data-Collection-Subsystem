import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['http://www.dtxsmuseum.com/']
    start_urls = ['http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1']
    base_domain = "http://www.dtxsmuseum.com"
    id_num: int=610910001
    mus_id_num: int=6109
    era_num = 'null'
    mus_name_num='大唐西市博物馆'
    def parse(self, response):
        #SelectorList对象
        duanzidivs = response.xpath("//div[@class='news-pic-list']/ul[@class='clearfix']/li")
        for duanzidiv in duanzidivs:
            #Selector对象
            id = self.id_num
            self.id_num+=1
            mus_id=self.mus_id_num
            era=self.era_num
            mus_name=self.mus_name_num
            name = duanzidiv.xpath(".//span[@class='title']//text()").get()
            print('#' * 40)
            print(name)
            print('#' * 40)
            image = duanzidiv.xpath(".//span[@class='pic thumbnail']/img/@src").get()
            image = self.base_domain + image
            img_url = duanzidiv.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_domain + img_url, callback=self.parse_detail, dont_filter=True,meta={"id":id,"mus_id":mus_id,"era":era,"mus_name":mus_name,"name": name, "image": image})
        next_url = response.xpath("//div[@class='digg clearfix']/a[last()]/@href").get()
        current = response.xpath("//div[@class='digg clearfix']/span[@class='current']//text()").get()
        print('#' * 40)
        print(next_url)
        print('#' * 40)
        int_current=int(current)
        if int_current >= 4:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        id = response.meta["id"]
        mus_id=response.meta["mus_id"]
        era=response.meta["era"]
        mus_name=response.meta["mus_name"]
        name = response.meta["name"]
        image = response.meta["image"]
        introduction = response.xpath("//div[@class='news-content']//font//text()").getall()
        #// *[ @ id = "form1"] / div[4] / div[2] / div[4] / div[3] / font
        print('*' * 40)
        print(introduction)
        print('*' * 40)
        introduction = "".join(introduction).strip()
        item = QsbkItem(id=id,mus_id=mus_id,era=era,mus_name=mus_name,name=name, image=image, introduction=introduction)
        yield item
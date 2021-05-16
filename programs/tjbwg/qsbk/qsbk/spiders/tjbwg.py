import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from ..items import QsbkItem
#from fake_useragent import UserAgent

#ua = UserAgent()
#headers = {'User-Agent':ua.random,'Referer':'http://www.dtxsmuseum.com/news_pic_list.aspx?category_id=24&page=1'}
class QsbkSpiderSpider(scrapy.Spider):
    name = 'tjbwg'
    allowed_domains = ['https://www.tjbwg.com']
    start_urls = ['https://www.tjbwg.com/cn/collection.aspx?TypeId=10934']
    base_domain = "https://www.tjbwg.com/cn/collection.aspx"
    base_nexturl = "https://www.tjbwg.com/cn/"
    base_nextpage = "https://www.tjbwg.com/cn/collection.aspx?TypeId="
    id_num: int=120110001
    mus_id_num: int=1201
    era_num = '年代：'
    mus_name_num='天津博物馆'
    int_current=1
    typeld=10929
    def parse(self, response):
        #SelectorList对象
        duanzidivs = response.xpath("//div[@class='prdList1']/ul[@class='clearfix']/li")
        for duanzidiv in duanzidivs:
            #Selector对象
            id = self.id_num
            self.id_num+=1
            mus_id=self.mus_id_num
            era=self.era_num
            mus_name=self.mus_name_num
            name = duanzidiv.xpath(".//h3[@class='c_h']//text()").get().strip()
            image = duanzidiv.xpath(".//div[@class='img']/img/@src").get()
            image = self.base_domain + image
            img_url = duanzidiv.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_nexturl + img_url, callback=self.parse_detail, dont_filter=True,meta={"id":id,"mus_id":mus_id,"era":era,"mus_name":mus_name,"name": name, "image": image})
        next_url = response.xpath("//div[@class='page']/a[@class='page-next']/@href").get()

        current_1 = response.xpath("//div[@class='page']/a[@class='cur']/text()").get()
        current_2 = response.xpath("//div[@class='page']/a[last()-2]/text()").get()
        print('#' * 40+'1')
        print(next_url)
        print(current_1)
        print(current_2)
        print('#' * 40+'2')
        if not current_2 or current_1 >= current_2:
            if self.typeld<=10934:
                self.typeld+=1
                print('#' * 40+'1')
                print(self.base_nextpage + str(self.typeld))
                print('#' * 40+'2')
                yield scrapy.Request(self.base_nextpage+ str(self.typeld),callback=self.parse,dont_filter=True)
            else:
                return
        else:
            next_url = (next_url).strip()
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        id = response.meta["id"]
        mus_id=response.meta["mus_id"]
        era=response.meta["era"]
        mus_name=response.meta["mus_name"]
        name = response.meta["name"]
        image = response.meta["image"]
        introduction = response.xpath("//div[@class='d_con']//text()").getall()
        introduction = "".join(introduction).strip()
        item = QsbkItem(id=id,mus_id=mus_id,era=era,mus_name=mus_name,name=name, image=image, introduction=introduction)
        yield item
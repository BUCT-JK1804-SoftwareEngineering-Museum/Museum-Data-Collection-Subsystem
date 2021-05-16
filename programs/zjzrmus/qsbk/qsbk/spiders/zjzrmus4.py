import json

from scrapy.selector import Selector
import scrapy

from ..items import QsbkItem

class ZjzrmusSpider(scrapy.Spider):
    name = 'zjzrmus4'
    allowed_domains = ['http://www.zmnh.com/']
    start_urls = ['http://www.zmnh.com/henryhtml/collection.html']
    base_url = "http://www.zmnh.com/web?"
    base_domin = "http://www.zmnh.com/"
    col_id_num: int=330210341
    mus_id_num:int=3302
    mus_name_num='浙江自然博物馆'
    def parse(self,response):
        #url = "http://www.zmnh.com/web?category=17&limit=16&dicType=1&page=1&keyWord="
        for page in range(1,2):
            url = self.base_url+"category=17&limit=16&dicType=4&page="+str(page)+"&keyWord="
            # print('#' * 40 + '1')
            # print(url)
            # print('#' * 40 + '2')
            body = json.dumps(
                {
                    "category":'17',
                    "limit":'16',
                    "dicType":'4',
                    "page":str(page),
                    "keyWord":'',
                }
            )
            yield scrapy.Request(url,body=body,callback=self.parse_action,dont_filter=True,meta={"page":page})

    def parse_action(self, response):
        jsonBodyss=response.json()
        jsonBodys = jsonBodyss['data']
        page = response.meta["page"]
        for jsonBody in jsonBodys:
            urlid = jsonBody['id']
            urlinfo = "http://www.zmnh.com/web/getInfo?limit=16&page=" + str(page) + "&category=17&id=" + str(urlid)
            # print('#' * 40 + '1')
            # print(urlinfo)
            # print('#' * 40 + '2')
            #
            yield scrapy.Request(urlinfo,callback=self.parse_info,dont_filter=True)
        pass

    def parse_info(self,response):
        jsoninfo=response.json()
        col_picture = jsoninfo['img']
        col_picture = self.base_domin + str(col_picture)
        col_era = jsoninfo['dicTypeName']
        content = jsoninfo['content']
        #col_name=Selector(text=content).xpath("//span[1]//text()").get()
        col_name=jsoninfo['title']
        col_info=Selector(text=content).xpath('string(.)').get().strip()
        col_info=str(col_info).replace("\u3000","").replace("\xa0","")
        # print('#' * 40 + '1')
        # print(col_picture)
        # print(col_era)
        # #print(content)
        # print(col_name)
        # print(col_info)
        # print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item

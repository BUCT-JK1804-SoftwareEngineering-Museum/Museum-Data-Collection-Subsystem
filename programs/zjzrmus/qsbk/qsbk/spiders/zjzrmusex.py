import json

from scrapy.selector import Selector
import scrapy

from ..items import QsbkexItem

class ZjzrmusSpider(scrapy.Spider):
    name = 'zjzrmusex'
    allowed_domains = ['http://www.zmnh.com/']
    start_urls = ['http://www.zmnh.com/lintezhan/zhanlan.html']
    base_url = "http://www.zmnh.com/web?"
    base_domin = "http://www.zmnh.com/"
    exh_id_num: int=330210001
    mus_id_num:int=3302
    mus_name_num='浙江自然博物馆'
    def parse(self,response):
        #url = "http://www.zmnh.com/web?category=17&limit=16&dicType=1&page=1&keyWord="
        for page in range(1,2):
            url = "http://www.zmnh.com/web/exhibition?pavilionId=0&page=1&limit=11"
            # print('#' * 40 + '1')
            # print(url)
            # print('#' * 40 + '2')
            body = json.dumps(
                {
                    "pavilionId":"0",
                    "page":"1",
                    "limit":"11"
                }
            )
            yield scrapy.Request(url,body=body,callback=self.parse_action,dont_filter=True)

    def parse_action(self, response):
        jsonBodyss=response.json()
        jsonBodys = jsonBodyss['data']
        for jsonBody in jsonBodys:
            exh_name = jsonBody['title']
            content=jsonBody['content']
            exh_info = Selector(text=content).xpath('string(.)').get().strip()
            exh_info = str(exh_info).replace("\u3000", "").replace("\xa0", "")
            exh_time = '常设展览'
            exh_picture = jsonBody['img']
            exh_picture=self.base_domin+str(exh_picture)
            # print('#' * 40 + '1')
            # print(exh_name)
            # print('#' * 40 + '2')
            item = QsbkexItem(exh_id=self.exh_id_num,exh_name=exh_name,mus_id=self.mus_id_num,mus_name=self.mus_name_num,exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
            self.exh_id_num+=1
            yield item
        pass
import scrapy
import json
from scrapy.selector import Selector
from ..items import QsbkexItem

class ShmusSpider(scrapy.Spider):
    name = 'shmusex'
    #allowed_domains = ['https://www.shanghaimuseum.net']
    start_urls = ['https://www.shanghaimuseum.net/mu/frontend/pg/display/offline-exhibit']
    exh_id_num: int=310110001
    mus_id_num: int=3101
    mus_name_num='上海博物馆'

    def parse(self, response):
        for i in range(1,7):#7
            data={
                    "limit":'20',
                    "page":str(i),
                    'params':{
                        "exhibitTypeCode": "OFFLINE_EXHIBITION",
                        "langCode": "CHINESE",
                    }
            }
            headers={
                'Host':'www.shanghaimuseum.net',
                'Content-Type':'application/json'
            }
            url="https://www.shanghaimuseum.net/mu/frontend/pg/display/search-exhibit"
            yield scrapy.Request(url=url,method='POST',dont_filter=True,headers=headers,body=json.dumps(data),callback=self.parse_page)
    def parse_page(self,response):
        preview=response.json()
        #print(preview)
        datas = preview['data']
        for data in datas:
            exh_name = data['name']
            # print('#' * 40 + '1')
            # print(col_name)
            # #print(data)
            # print('#' * 40 + '2')
            exh_time=data['exhibitDateRange']
            exh_picture = data['picPath']
            exh_picture = "https://www.shanghaimuseum.net/mu/" + str(exh_picture)
            exh_info="展览地点："+data['exhibitPlace']
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_era)
            # print(col_picture)
            # print(col_info)
            # print('#' * 40 + '2')
            item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num,
                              mus_name=self.mus_name_num,
                              exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
            self.exh_id_num += 1
            yield item
        pass
import scrapy
import json
from scrapy.selector import Selector
from ..items import QsbkItem

class ShmusSpider(scrapy.Spider):
    name = 'shmus'
    #allowed_domains = ['https://www.shanghaimuseum.net']
    start_urls = ['https://www.shanghaimuseum.net/mu/frontend/pg/collection/antique']
    col_id_num: int=310110001
    mus_id_num: int=3101
    mus_name_num='上海博物馆'

    def parse(self, response):
        for i in range(1,76):#76
            data={
                    "limit":'20',
                    "page":str(i),
                    'params':{
                        "antiqueSourceCode": "ANTIQUE_SOURCE_1",
                        "langCode": "CHINESE",
                    }
            }
            headers={
                'Host':'www.shanghaimuseum.net',
                'Content-Type':'application/json'
            }
            url="https://www.shanghaimuseum.net/mu/frontend/pg/collection/search-antique"
            yield scrapy.Request(url=url,method='POST',dont_filter=True,headers=headers,body=json.dumps(data),callback=self.parse_page)
    def parse_page(self,response):
        preview=response.json()
        #print(preview)
        datas = preview['data']
        for data in datas:
            col_name = data['name']
            # print('#' * 40 + '1')
            # print(col_name)
            # #print(data)
            # print('#' * 40 + '2')
            catalog = data['catalog']
            col_era = Selector(text=catalog).xpath("//p[1]//text()").get().strip()
            col_era = str(col_era).replace("（", "")
            col_picture = data['picPath']
            col_picture = "https://www.shanghaimuseum.net/mu/" + str(col_picture)
            description = data['description']
            col_info = Selector(text=description).xpath('string(.)').get().strip()
            col_info = str(col_info).replace("\xa0", "").replace("\n", "").replace("\r", "").replace("\n", "")
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_era)
            # print(col_picture)
            # print(col_info)
            # print('#' * 40 + '2')
            item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                            col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
            self.col_id_num += 1
            yield item
        pass
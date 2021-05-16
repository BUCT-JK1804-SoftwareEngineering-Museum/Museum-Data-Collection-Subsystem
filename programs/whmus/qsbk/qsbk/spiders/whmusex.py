import scrapy
import json
from scrapy.selector import Selector
from ..items import QsbkexItem

class WhmusSpider(scrapy.Spider):
    name = 'whmusex'
    allowed_domains = ['https://www.whmuseum.com.cn']
    start_urls = ['https://www.whmuseum.com.cn/japi/sw-cms/api/queryExhibitionTempList']
    exh_id_num: int = 420310001
    mus_id_num: int = 4203
    mus_name_num = '武汉博物馆'

    def parse(self, response):
        for i in range(0,21):#21
            data={
                'entity':{
                    'type':"cms0701"
                },
                'param':{
                    'pageNum':str(i),
                    'pageSize':'4',
                    'str':"",
                    'type':""
                }
            }
            headers = {
                'Host': 'www.whmuseum.com.cn',
                'Content-Type': 'application/json;charset=UTF-8'
            }
            url = "https://www.whmuseum.com.cn/japi/sw-cms/api/queryExhibitionTempList"
            yield scrapy.Request(url=url, method='POST', dont_filter=True, headers=headers, body=json.dumps(data),
                                 callback=self.parse_page)
        pass
    def parse_page(self,response):
        print(response)
        preview=response.json()
        print(preview)
        records=preview['data']['records']
        for record in records:
            exh_name=record['tempName']
            exh_name=str(exh_name).replace("\r","").replace("\n","")
            exh_time=record['startTime']+"至"+record['endTime']
            exh_picture=record['thumb']
            exh_picture="https://www.whmuseum.com.cn/file/"+str(exh_picture)
            description = record['description']
            exh_info = Selector(text=description).xpath('string(.)').get().strip()
            exh_info = str(exh_info).replace("\xa0", "").replace("\n", "").replace("\r", "").replace("\n", "").replace(" ","").replace("'","")
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
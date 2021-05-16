import scrapy
import json
from scrapy.selector import Selector
from ..items import QsbkItem

class WhmusSpider(scrapy.Spider):
    name = 'whmus'
    allowed_domains = ['https://www.whmuseum.com.cn']
    start_urls = ['https://www.whmuseum.com.cn/japi/sw-cms/api/queryExhibitList']
    col_id_num: int = 420310001
    mus_id_num: int = 4203
    mus_name_num = '武汉博物馆'

    def parse(self, response):
        kind=['ceramics','bronze','jade','calligraphy',
              'painting','sculpture','bamboo','col-other']
        page_num=[7,3,4,1,5,1,1,1]
        for i in range(0,8):#8
            for j in range(1,page_num[i]+1):
                data={
                    'entity':{
                        "exhibitLevel":"",
                        "exhibitName":"",
                        "exhibitType":str(kind[i])
                    },
                    'param':{
                        "pageNum":str(j),
                        "pageSize":'8'
                    }
                }
                headers = {
                    'Host': 'www.whmuseum.com.cn',
                    'Content-Type': 'application/json;charset=UTF-8'
                }
                url = "https://www.whmuseum.com.cn/japi/sw-cms/api/queryExhibitList"
                yield scrapy.Request(url=url, method='POST', dont_filter=True, headers=headers, body=json.dumps(data),
                                     callback=self.parse_page)
        pass
    def parse_page(self,response):
        print(response)
        preview=response.json()
        records=preview['data']['records']
        for record in records:
            col_name=record['exhibitName']
            col_era=record['age']
            col_picture=record['appThumb']
            col_picture="https://www.whmuseum.com.cn/file/"+str(col_picture)
            description = record['description']
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
import scrapy

import json

class JxsmusSpider(scrapy.Spider):
    name = 'jxsmus2'
    #allowed_domains = ['http://www.jxmuseum.cn']
    start_urls = ['http://www.jxmuseum.cn/api/sw-cms/api/queryExhibitList']

    def parse(self, response):
        kind=['qtq','tcq','ysq','jyq','zh']
        page_num=[2,3,3,2,1]
        for i in range(0,1):#5
            for j in range(1,page_num[i]+1):
                data={
                    'entity':{
                        'exhibitType':kind[i],
                        'languageType':'CN',
                        'publishPlatform':'PT',
                    },
                    'param':{
                        'pageNum':str(j),
                        'pageSize':'8',
                    }
                }
                headers = {
                    'Host': 'www.jxmuseum.cn',
                    'Content-Type': 'application/json'
                }
                url="http://www.jxmuseum.cn/api/sw-cms/api/queryExhibitList"
                print(data)
                yield scrapy.Request(url=url, method='POST', dont_filter=True, headers=headers, body=json.dumps(data),
                                     callback=self.parse_page)
        pass
    def parse_page(self,response):
        preview=response.json()
        print('#' * 40 + '1')
        print(preview)
        print('#' * 40 + '2')
        # records=preview['records']
        # for record in records:
        #     col_name=record['exhibitName']
        #     print('#' * 40 + '1')
        #     print(col_name)
        #     print('#' * 40 + '2')
        pass
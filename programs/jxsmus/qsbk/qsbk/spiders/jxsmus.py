import scrapy
import requests
from requests.auth import HTTPBasicAuth

import json

class JxsmusSpider(scrapy.Spider):
    name = 'jxsmus'
    #allowed_domains = ['http://www.jxmuseum.cn']
    start_urls = ['http://www.jxmuseum.cn']

    def parse(self, response):
        kind=['qtq','tcq','ysq','jyq','zh']
        page_num=[2,3,3,2,1]
        for i in range(0,1):#5
            for j in range(1,page_num[i]+1):
                page_url="http://www.jxmuseum.cn/collection/ztsc/"+kind[i]+"?page="+str(j)
                data = {
                    'entity': {
                        'exhibitType':str(kind[i]),
                        'languageType': 'CN',
                        'publishPlatform': 'PT',
                    },
                    'param': {
                        'pageNum':str(j),
                        'pageSize':'8',
                    }
                }
                headers = {
                    'Host': 'www.jxmuseum.cn',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Wzws-Ray': '1129-1620494048.749-w-waf03tjgt',
                }
                url = "http://www.jxmuseum.cn/api/sw-cms/api/queryExhibitList"
                # print(data)
                # r=requests.get(url,verify=True,auth=('user','pass'))
                # print(r)
                yield scrapy.Request(url=url,method='POST',dont_filter=True, headers=headers, body=json.dumps(data),
                                     callback=self.parse_page)
                # yield requests.get(url=url,auth=HTTPBasicAuth('wuya', 'admin'),method='POST', dont_filter=True, headers=headers, body=json.dumps(data),
                #                       callback=self.parse_page)
        pass
    def parse_page(self,response):
        print(response)
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
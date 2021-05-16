import json

import scrapy
from scrapy.selector import Selector
from ..items import QsbkItem

class CdwhcmusSpider(scrapy.Spider):
    name = 'cdwhcmus'
    allowed_domains = ['http://www.wuhouci.net.cn']
    start_urls = ['http://www.wuhouci.net.cn/wwjc.html?page=1']
    col_id_num: int = 510310001
    mus_id_num: int = 5103
    mus_name_num='成都武侯祠博物馆'

    def parse(self, response):
        for i in range(1,3):
            body=json.dumps(
                {
                    "page":str(i),
                    "pageSize":"8",
                }
            )
            page_url="http://www.wuhouci.net.cn/essence/list.html?page="+str(i)+"&pageSize=8"
            yield scrapy.Request(page_url,body=body,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        jsonlists=response.json()['data']['list']
        for jsonlist in jsonlists:
            body=json.dumps(
                {
                    "id":str(jsonlist['id']),
                }
            )
            info_url="http://www.wuhouci.net.cn/essence/detail.html?id="+str(jsonlist['id'])
            # print('#' * 40 + '1')
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(info_url,body=body,callback=self.parse_info2,dont_filter=True)

    def parse_info2(self,response):
        print(response)
        jsondatas = response.json()
        jsondata=jsondatas['data']

        col_name=jsondata['title']
        col_picture="http://www.wuhouci.net.cn"+str(jsondata['face'])
        content=jsondata['content']
        col_info=Selector(text=content).xpath('string(.)').get().strip()
        col_info=str(col_info).replace("\xa0","").replace("\n","").replace("\r","").replace("\n","")
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era="",
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
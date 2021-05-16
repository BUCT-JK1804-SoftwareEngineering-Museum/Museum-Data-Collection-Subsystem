import scrapy
import json
from ..items import QsbkexItem

class BmymusexSpider(scrapy.Spider):
    name = 'bmymusex'
    allowed_domains = ['http://www.bmy.com.cn']
    start_urls = ['http://www.bmy.com.cn/bmy-websitems-1.0-SNAPSHOT/bmy/list.do?currentPage=1&showCount=2&code=005003003']
    exh_id_num:int =610210001
    mus_id_num:int =6102
    mus_name_num = '秦始皇帝陵博物院'

    def parse(self, response):
        for i in range(1,7):
            url="http://www.bmy.com.cn/bmy-websitems-1.0-SNAPSHOT/bmy/list.do?currentPage="+str(i)+"&showCount=2&code=005003003"
            body=json.dumps(
                {
                    "currentPage":str(i),
                    "showCount":'2',
                    "code":'005003003'
                }
            )
            yield scrapy.Request(url,body=body,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        preview=response.json()
        lists=preview['list']
        for list in lists:
            exh_name=list['title']
            exh_time=list['name']
            exh_info='3D展览'
            exh_picture="http://www.bmy.com.cn/file/"+list['picture']
            # print('#' * 40 + '1')
            # print(exh_name)
            # print(exh_time)
            # print(exh_info)
            # print(exh_picture)
            # print('#' * 40 + '2')
            item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num,
                              mus_name=self.mus_name_num, exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
            self.exh_id_num += 1
            yield item
        pass
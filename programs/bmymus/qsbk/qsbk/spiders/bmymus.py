import scrapy
import json

from ..items import QsbkItem
class BmymusSpider(scrapy.Spider):
    name = 'bmymus'
    allowed_domains = ['http://www.bmy.com.cn']
    start_urls = ['http://www.bmy.com.cn/bmy-websitems-1.0-SNAPSHOT/bmy/searchlist.do?currentPage=1&showCount=15']
    col_id_num: int=610210001
    mus_id_num: int=6102
    mus_name_num='秦始皇帝陵博物院'

    def parse(self, response):
        url="http://www.bmy.com.cn/bmy-websitems-1.0-SNAPSHOT/bmy/searchlist.do?currentPage=1&showCount=15"
        body=json.dumps(
            {
                "currentPage":1,
                "showCount":15,
            }
        )
        yield scrapy.Request(url,body=body,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        preview=response.json()
        lists=preview['list']
        timeslists=preview['timesList']
        for i in range(0,6):
            col_name=lists[i]['title']
            col_picture="http://www.bmy.com.cn"+lists[i]['path']
            col_era=timeslists[i]['name']
            col_info='无头'
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(col_era)
            # print('#' * 40 + '2')
            item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                            col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
            self.col_id_num += 1
            yield item
        pass
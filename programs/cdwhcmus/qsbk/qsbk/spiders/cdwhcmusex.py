import json
import scrapy

from scrapy.selector import Selector

from ..items import QsbkexItem

class CdwhcmusSpider(scrapy.Spider):
    name = 'cdwhcmusex'
    #allowed_domains = ['http://www.wuhouci.net.cn']
    start_urls = ['http://www.wuhouci.net.cn/exhibition/list.html?time=0&category_id=0&page=1&pageSize=8']

    exh_id_num: int =510310001
    mus_id_num: int =5103
    mus_name_num='成都武侯祠博物馆'

    def parse(self, response):
        #url="http://www.wuhouci.net.cn/exhibition/list.html?time=0&category_id=0&page=1&pageSize=8"
        for i in range(1,6):
            body=json.dumps(
                {
                    "time":"0",
                    "category_id":"0",
                    "page":str(i),
                    "pageSize":"8",
                }
            )
            url="http://www.wuhouci.net.cn/exhibition/list.html?time=0&category_id=0&page="+str(i)+"&pageSize=8"
            yield scrapy.Request(url,body=body,callback=self.parse_page,dont_filter=True)

    def parse_page(self,response):
        jsondatas=response.json()
        jsondata=jsondatas['data']
        jsonlists=jsondata['exhibition_list']
        #info_url="http://www.wuhouci.net.cn/ztzl-detail.html"
        for jsonlist in jsonlists:
            exh_name=jsonlist['exhibition_theme']
            exh_time=jsonlist['exhibition_time']
            info_id=jsonlist['exhibition_id']
            body=json.dumps(
                {
                    "id":str(info_id)
                }
            )
            # print('#' * 40 + '1')
            # print(exh_name)
            # print(exh_time)
            # print('#' * 40 + '2')
            info_url="http://www.wuhouci.net.cn/exhibition/info.html?id="+str(info_id)
            yield scrapy.Request(info_url,body=body,callback=self.parse_info,meta={"exh_name":exh_name,"exh_time":exh_time})
            pass
        pass
    def parse_info(self,response):
        josndatas=response.json()
        jsondata=josndatas['data']['exhibition_info']
        exh_name=response.meta['exh_name']
        exh_time=response.meta['exh_time']
        base_picture="http://www.wuhouci.net.cn"
        exh_picture=base_picture+str(jsondata['exhibition_img'])
        content=jsondata['exhibition_content']
        exh_info=Selector(text=content).xpath('string(.)').get().strip()
        exh_info=str(exh_info).replace("\xa0","").replace(" ","").replace("\n","")
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
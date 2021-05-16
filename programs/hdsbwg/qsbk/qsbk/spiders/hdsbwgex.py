import urllib.parse

from bs4 import BeautifulSoup

import scrapy

from ..items import QsbkexItem


class HandanSpider(scrapy.Spider):
    name = 'hdsbwgex'
    allowed_domains = ['https://www.hdmuseum.org/']
    start_urls = ['https://www.hdmuseum.org/Product/Query']
    base_url="https://www.hdmuseum.org"
    exh_id_num:int=130310001
    mus_id_num:int=1303
    mus_name_num='邯郸市博物馆'
    def start_requests(self):
        url = "https://www.hdmuseum.org/Product/Query"
        requests=[]
        for i in range(1, 3):
            data = {
                'bigClassId':'2',
                'classId':'15',
                'isTemp':str(i),
                'pageIndex':'1',
            }
            request = scrapy.FormRequest(url, formdata=data, callback=self.parse_page)
            requests.append(request)
        return requests
    def parse_page(self,response):
        jsonBody =response.json()
        models=jsonBody['list']
        for dict in models:
            exh_name=dict['productName']
            exh_picture=self.base_url+dict['img']
            exh_info=dict['productContent']
            exh_time=dict['updateTime']
            exh_info=urllib.parse.unquote(exh_info)
            soup= BeautifulSoup(exh_info,'html.parser')
            exh_info=soup.get_text().strip()
            if not exh_info:
                exh_info="无"
            exh_info=exh_info.replace("\n","").replace("\xa0","")
            print(exh_info)
            # print('#' * 40 + '1')
            # print(exh_name)
            # print(exh_info)
            # print(exh_time)
            # print('#' * 40 + '2')
            item=QsbkexItem(exh_id=self.exh_id_num,exh_name=exh_name,mus_id=self.mus_id_num,mus_name=self.mus_name_num,exh_info=exh_info,exh_picture=exh_picture,exh_time=exh_time)
            self.exh_id_num += 1
            yield item

import scrapy

from ..items import QsbkItem

class HandanSpider(scrapy.Spider):
    name = 'handan'
    allowed_domains = ['https://www.hdmuseum.org/']
    start_urls = ['https://www.hdmuseum.org/Product/Query']
    base_url="https://www.hdmuseum.org"
    col_id_num:int=130310001
    mus_id_num:int=1303
    col_era_num='年代：'
    mus_name_num='邯郸市博物馆'
    def start_requests(self):
        url = "https://www.hdmuseum.org/Product/Query"
        requests=[]
        for i in range(1, 4):
            data = {
                'classId': '16',
                'pageIndex': str(i),
                'pageSize': '9',
            }
            request = scrapy.FormRequest(url, formdata=data, callback=self.parse_page)
            requests.append(request)
        return requests
    def parse_page(self,response):
        jsonBody =response.json()
        models=jsonBody['list']
        for dict in models:
            col_name=dict['productName']
            col_picture=self.base_url+dict['img']
            col_info=dict['description']
            item=QsbkItem(col_id=self.col_id_num,mus_id=self.mus_id_num,col_name=col_name,col_era=self.col_era_num,col_info=col_info,mus_name=self.mus_name_num,col_picture=col_picture)
            self.col_id_num += 1
            yield item
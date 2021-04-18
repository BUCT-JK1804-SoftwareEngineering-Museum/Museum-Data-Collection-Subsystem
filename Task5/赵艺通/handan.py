
import scrapy

from ..items import HandanItem

class HandanSpider(scrapy.Spider):
    name = 'handan'
    allowed_domains = ['https://www.hdmuseum.org/']
    start_urls = ['https://www.hdmuseum.org/Product/Query']
    base_url="https://www.hdmuseum.org"

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
            id=dict['id']
            productName=dict['productName']
            img=self.base_url+dict['img']
            description=dict['description']
            item=HandanItem(id=id,productName=productName,img=img,description=description)
            yield item
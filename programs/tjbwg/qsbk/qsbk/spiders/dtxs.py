
import scrapy

from ..items import QsbkItem

class HandanSpider(scrapy.Spider):
    name = 'dtxs'
    allowed_domains = ['http://www.dtxsmuseum.com/']
    start_urls = ['http://www.dtxsmuseum.com/tools/submit_ajax.ashx?action=user_check_login']
    base_url="http://www.dtxsmuseum.com"

    def start_requests(self):
        url = "http://www.dtxsmuseum.com/tools/submit_ajax.ashx?action=user_check_login"
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

        yield scrapy.Request(self.base_domain + img_url, callback=self.parse_detail, dont_filter=True,meta={"name": name, "image": image})
        next_url = response.xpath("//ul[@class='page-box']/div[@class='digg clearfix']/a/@href").get()
        if not next_url:

            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse, dont_filter=True)
    def parse_page(self,response):
        jsonBody =response.json()
        models=jsonBody['list']
        for dict in models:
            id=dict['id']
            productName=dict['productName']
            img=self.base_url+dict['img']
            description=dict['description']
            item=QsbkItem(id=id,productName=productName,img=img,description=description)
            yield item
import scrapy

from ..items import QsbkItem

class QzmusSpider(scrapy.Spider):
    name = '1911mus'
    allowed_domains = ['http://wlt.hubei.gov.cn']
    start_urls = ['http://wlt.hubei.gov.cn/1911museum/wwzz/zs/202005/t20200521_2282570.html']
    col_id_num: int = 420210001
    mus_id_num: int = 4202
    mus_name_num = '辛亥革命武昌起义纪念馆'

    def parse(self, response):
        musdivs=response.xpath("//div[@class='article']").get()
        print(musdivs)
        pass
import scrapy
from urllib.parse import quote
from ..items import QsbkItem

class JsyzmusSpider(scrapy.Spider):
    name = 'jsyzmus'
    allowed_domains = ['http://www.jinshasitemuseum.com']
    start_urls = ['http://www.jinshasitemuseum.com/Treasure/Index?nodeName=金银器']
    col_id_num: int=510710001
    mus_id_num: int=5107
    mus_name_num='成都金沙遗址博物馆'

    def parse(self, response):
        nodeName=['金银器','玉石器、宝石','铜器','陶器','竹木雕','石器、石刻、砖瓦']
        for i in range(0,6):
            kind_url="http://www.jinshasitemuseum.com/Treasure/Index?nodeName="+quote(nodeName[i])
            yield scrapy.Request(kind_url,callback=self.parse_kind,dont_filter=True)
        pass
    def parse_kind(self,response):
        jsdivs=response.xpath("//div[@class='treasures-list container']/ul/li")
        for jsdiv in jsdivs:
            col_name=jsdiv.xpath(".//p/@title").get()
            col_picture=jsdiv.xpath(".//div/img/@src").get()
            col_picture=str(col_picture)
            col_era='商周'
            col_info=jsdiv.xpath(".//div/img/@name2").get()
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(col_era)
            # print(col_info)
            # print('#' * 40 + '2')
            item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                            col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
            self.col_id_num += 1
            yield item
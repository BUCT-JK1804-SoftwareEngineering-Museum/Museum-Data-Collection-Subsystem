import scrapy

from ..items import QsbkItem

class WfsmusSpider(scrapy.Spider):
    name = 'wfsmus'
    allowed_domains = ['http://www.wfsbwg.com']
    start_urls = ['http://www.wfsbwg.com/list/?5_1.html']
    base_next_page="http://www.wfsbwg.com/list/"
    base_col_picture="http://www.wfsbwg.com"
    col_id_num: int = 370710001
    mus_id_num: int = 3707
    mus_name_num = '潍坊市博物馆'

    def parse(self, response):
        wfsdivs=response.xpath("//div[@class='list_contentt']/ul/li")
        for wfsdiv in wfsdivs:
            col_name = wfsdiv.xpath(".//div/a/@title").get()
            col_picture= wfsdiv.xpath(".//div/a/img/@src").get()
            col_picture=self.base_col_picture+str(col_picture)
            col_info='无'
            col_era='见名字或不详'
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print('#' * 40 + '2')
            item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                            col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
            self.col_id_num += 1
            yield item
            pass
        now_page = response.xpath("//div[@class='digg4 metpager_8']/span/font/text()").get()
        if int(now_page)>=10:
            return
        else:
            next_page=response.xpath("//div[@class='digg4 metpager_8']/a[last()-1]/@href").get()
            # print('#' * 40 + '1')
            # print(self.base_next_page+str(next_page))
            # print('#' * 40 + '2')
            yield scrapy.Request(self.base_next_page+str(next_page),callback=self.parse,dont_filter=True)
        pass

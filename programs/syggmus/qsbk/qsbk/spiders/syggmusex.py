import scrapy

from ..items import QsbkexItem

class SyggmusSpider(scrapy.Spider):
    name = 'syggmusex'
    allowed_domains = ['http://www.sypm.org.cn']
    start_urls = ['http://www.sypm.org.cn/products_list2/pmcId=54&pageNo_FrontProducts_list01-0041=1&pageSize_FrontProducts_list01-0041=16.html']
    exh_id_num: int=210510001
    mus_id_num: int=2105
    mus_name_num='沈阳故宫博物院'

    def parse(self, response):
        for i in range(1,6):#6
            page_url="http://www.sypm.org.cn/products_list2/pmcId=54&pageNo_FrontProducts_list01-0041="+str(i)+"&pageSize_FrontProducts_list01-0041=16.html"
            # print('#' * 40 + '1')
            # print(page_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        sydivs=response.xpath("//ul[@class='mainul productlist-02']/li[@class='content column-num4']")
        for sydiv in sydivs:
            exh_name=sydiv.xpath(".//div[@class='pic-module']//a/@title").get()
            exh_picture=sydiv.xpath(".//div[@class='pic-module']//img/@src").get()
            info_url=sydiv.xpath(".//div[@class='pic-module']//a/@href").get()
            exh_picture="http://www.sypm.org.cn"+exh_picture
            # print('#' * 40 + '1')
            # print(exh_name)
            # print(exh_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request("http://www.sypm.org.cn"+info_url,callback=self.parse_info,dont_filter=True,
                                 meta={"col_name":exh_name,"col_picture":exh_picture})
        pass
    def parse_info(self,response):
        exh_name=response.meta['col_name']
        exh_picture=response.meta['col_picture']
        exh_info=response.xpath("//div[@id='FrontProducts_detail02-0011_cont_1']//text()").getall()
        exh_info=str(exh_info).strip().replace("\u3000","").replace("\n","").replace("\t","").replace("\\n","").replace("\\t","").replace("\\xa0","").replace("'","").replace(" ","").replace(",,","").replace("\\u3000","")
        exh_time='临时展览'
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_info)
        # print(col_era)
        # print('#' * 40 + '2')
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
        pass
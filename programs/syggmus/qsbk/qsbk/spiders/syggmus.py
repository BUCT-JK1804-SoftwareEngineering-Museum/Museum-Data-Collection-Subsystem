import scrapy

from ..items import QsbkItem

class SyggmusSpider(scrapy.Spider):
    name = 'syggmus'
    allowed_domains = ['http://www.sypm.org.cn']
    start_urls = ['http://www.sypm.org.cn/products_list3/&pmcId=77&comp_stats=comp-FrontProductsCategory_show01-ycjd&pageNo_FrontProducts_list01-0042=1&pageSize_FrontProducts_list01-0042=20.html']
    col_id_num: int=210510001
    mus_id_num: int=2105
    mus_name_num='沈阳故宫博物院'

    def parse(self, response):
        for i in range(1,41):#41
            page_url="http://www.sypm.org.cn/products_list3/&pmcId=77&comp_stats=comp-FrontProductsCategory_show01-ycjd&pageNo_FrontProducts_list01-0042="+str(i)+"&pageSize_FrontProducts_list01-0042=20.html"
            # print('#' * 40 + '1')
            # print(page_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        sydivs=response.xpath("//ul[@class='mainul productlist-02']/li[@class='content column-num4']")
        for sydiv in sydivs:
            col_name=sydiv.xpath(".//div[@class='pic-module']//a/@title").get()
            col_picture=sydiv.xpath(".//div[@class='pic-module']//img/@src").get()
            info_url=sydiv.xpath(".//div[@class='pic-module']//a/@href").get()
            col_picture="http://www.sypm.org.cn"+col_picture
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request("http://www.sypm.org.cn"+info_url,callback=self.parse_info,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@id='FrontProducts_detail02-0012_cont_1']//text()").get()
        col_info=str(col_info).strip().replace("\u3000","").replace("\n","").replace("\t","")
        col_era='见介绍'
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_info)
        # print(col_era)
        # print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
        pass
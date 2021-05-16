import scrapy
from ..items import QsbkexItem

class RjzygmmusexSpider(scrapy.Spider):
    name = 'rjzygmmusex'
    allowed_domains = ['http://www.rjjng.com.cn']
    start_urls = ['http://www.rjjng.com.cn/list.thtml?id=10948']
    exh_id_num: int= 360310001
    mus_id_num: int=3603
    mus_name_num='瑞金中央革命根据地纪念馆'

    def parse(self, response):
        for i in range(1,11):#11
            page_url="http://www.rjjng.com.cn/list.thtml?id=10948&&pn="+str(i)
            # print('#' * 40 + '1')
            # print(page_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
        pass
    def parse_page(self,response):
        exdivs=response.xpath("//div[@class='list']/ul/li")
        #print(exdivs)
        for exdiv in exdivs:
            info_url=exdiv.xpath(".//a/@href").get()
            # print('#' * 40 + '1')
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True)
        pass
    def parse_info(self,response):
        exh_name=response.xpath("//div[@class='nr']/h2/text()").get()
        if not exh_name:
            return
        exh_picture=response.xpath("//div[@class='cont']//a[1]/@href").get()
        exh_info=response.xpath("//div[@class='cont']//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_info=str(exh_info).replace("\n","").replace("\xa0","").replace(" ","").replace("\r","")
        #exh_time=response.xpath("//div[@class='cont']//strong[contains(text(),'时间')]//text()").get()
        if not exh_info:
            exh_info='无'
            exh_time='临时展览'
        exh_time='见介绍'
        # print('#' * 40 + '1')
        # print(exh_name)
        # print(exh_picture)
        # print(exh_info)
        # print(exh_time)
        # print('#' * 40 + '2')
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
        pass
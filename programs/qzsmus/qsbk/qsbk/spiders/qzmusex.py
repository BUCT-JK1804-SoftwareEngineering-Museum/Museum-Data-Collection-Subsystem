import scrapy

from ..items import QsbkexItem

class QzmusSpider(scrapy.Spider):
    name = 'qzmusex'
    allowed_domains = ['http://www.qingzhoumuseum.cn']
    start_urls = ['http://www.qingzhoumuseum.cn/zl/jbcl']
    exh_id_num: int = 370410001
    mus_id_num: int = 3704
    mus_name_num = '青州博物馆'

    def parse(self, response):
        kind = ['jbcl/', 'lszl/']
        page_num = [2, 9]
        for i in range(0,1):#2
            kind_url="http://www.qingzhoumuseum.cn/zl/"+str(kind[i])
            # print('#' * 40 + '1')
            # print(kind[i])
            # print(kind_url)
            # print('#' * 40 + '2')
            page=["index.html","index_1.html","index_2.html","index_3.html","index_4.html",
                  "index_5.html","index_6.html","index_7.html","index_8.html"]
            for j in range(0,int(page_num[i])):
                page_url=kind_url+page[j]
                # print('#' * 40 + '1')
                # print(page_url)
                # print('#' * 40 + '2')
                yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True,meta={"kind":kind_url})
        pass
    def parse_page(self,response):
        kind=response.meta['kind']
        exdivs=response.xpath("//div[2]/table/tbody/tr[last()]//table")
        for exdiv in exdivs:
            exh_name=exdiv.xpath(".//tr[1]//span[@class='title2']/text()").get()
            exh_picture=exdiv.xpath(".//tr[1]//img/@src").get()
            exh_picture=exh_picture[2:]
            exh_picture=kind+exh_picture

            info_url=exdiv.xpath(".//tr[1]/td[1]/a/@href").get()
            info_url=info_url[2:]
            info_url=kind+info_url
            print('#' * 40 + '1')
            print(exh_name)
            print(exh_picture)
            print(info_url)
            print('#' * 40 + '2')
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"exh_name":exh_name,"exh_picture":exh_picture})
        pass
    def parse_info(self,response):
        exh_name=response.meta['exh_name']
        exh_name=str(exh_name).replace("\n","").replace(" ","")
        exh_picture=response.meta['exh_picture']
        exh_time=response.xpath("//div[2]/table/tbody//tr[2]//a[last()]/@title").get()
        exh_info = response.xpath("//div[2]/table/tbody//tr[4]//text()").getall()
        exh_info="".join(exh_info).strip().replace("\n","").replace("\xa0","").replace(" ","").replace("\t","")
        # print('#' * 40 + '1')
        # print(exh_name)
        # print(exh_picture)
        # print(exh_time)
        # print(exh_info)
        # print('#' * 40 + '2')
        item = QsbkexItem(exh_id=self.exh_id_num, exh_name=exh_name, mus_id=self.mus_id_num, mus_name=self.mus_name_num,
                          exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        self.exh_id_num += 1
        yield item
        pass
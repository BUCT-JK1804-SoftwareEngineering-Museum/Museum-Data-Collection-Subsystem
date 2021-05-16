import scrapy

from ..items import QsbkItem

class RjzygmmusSpider(scrapy.Spider):
    name = 'rjzygmmus'
    allowed_domains = ['http://www.rjjng.com.cn']
    start_urls = ['http://www.rjjng.com.cn/cangpin.thtml?id=10950&&pn=1']
    col_id_num: int=360310001
    mus_id_num: int=3606
    mus_name_num='瑞金中央革命根据地纪念馆'

    def parse(self, response):
        kind_page=[7,5,6,1,1]
        j=0
        for i in range(10950,10955):#10955
            # print('#' * 40 + '1')
            # print(i)
            # print(kind_page[j])
            # print('#' * 40 + '2')
            for k in range(1,int(kind_page[j])+1):
                page_url="http://www.rjjng.com.cn/cangpin.thtml?id="+str(i)+"&&pn="+str(k)
                # print('#' * 40 + '1')
                # print(page_url)
                # print('#' * 40 + '2')
                yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
                pass
            j+=1
        pass
    def parse_page(self,response):
        rjdivs=response.xpath("//div[@class='list']/ul/li")
        for rjdiv in rjdivs:
            col_name=rjdiv.xpath(".//div[@class='c']/text()").get()
            col_picture=rjdiv.xpath(".//img/@src").get()
            info_url=rjdiv.xpath(".//a/@href").get()
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='cont']//text()").getall()
        col_info="".join(col_info).strip()
        col_info=str(col_info).replace("\n","").replace("\xa0","")
        print('#' * 40 + '1')
        print(col_name)
        print(col_picture)
        print(col_info)
        print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era="土地革命战争时期",
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
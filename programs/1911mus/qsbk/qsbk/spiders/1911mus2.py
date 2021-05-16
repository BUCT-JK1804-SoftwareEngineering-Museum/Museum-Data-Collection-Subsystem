import scrapy

from ..items import QsbkItem

class QzmusSpider(scrapy.Spider):
    name = '1911mus2'
    #allowed_domains = ['http://wlt.hubei.gov.cn']
    start_urls = ['http://wlt.hubei.gov.cn/1911museum/wwzz/cq/']
    col_id_num: int = 420210001
    mus_id_num: int = 4202
    mus_name_num = '辛亥革命武昌起义纪念馆'

    def parse(self, response):
        kind = ['cq/', 'hz/', 'jp/', 'sk/', 'sh/', 'zj/', 'zz/']
        page_num = [1, 2, 1, 2, 2, 2, 1]
        for i in range(0,1):#7
            kind_url="http://wlt.hubei.gov.cn/1911museum/wwzz/"+kind[i]
            # print('#' * 40 + '1')
            # print(kind_url)
            # print('#' * 40 + '2')
            page=['index.shtml','index_1.shtml']
            for j in range(0,page_num[i]):
                page_url=kind_url+page[j]
                print('#' * 40 + '1')
                print(page_url)
                print('#' * 40 + '2')
                yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
            pass
    def parse_page(self,response):
        #print(kind_url)
        print(response)
        divs=response.xpath("//div[@class='pane']")
        ul=response.xpath("/html/body/div/div[3]/div/div/ul")
        print(ul)
        # for div in divs:
        #     col_name=div.xpath(".//a/@title").get()
        #     col_picture=div.xpath(".//img/@src").get()
        #     col_picture=col_picture[2:]
        #     col_picture=kind_url+str(col_picture)
        #     print('#' * 40 + '1')
        #     print(col_name)
        #     print(col_picture)
        #     print('#' * 40 + '2')
        pass


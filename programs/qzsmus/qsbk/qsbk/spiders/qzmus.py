import scrapy

from ..items import QsbkItem

class QzmusSpider(scrapy.Spider):
    name = 'qzmus'
    allowed_domains = ['http://www.qingzhoumuseum.cn']
    start_urls = ['http://www.qingzhoumuseum.cn/cp/tq']
    col_id_num: int = 370410001
    mus_id_num: int = 3704
    mus_name_num = '青州博物馆'

    def parse(self, response):
        kind = ['tq/', 'cq/', 'sh/', 'yq/', 'qtq/', 'sk/', 'lxs/', 'qt/']
        page_num = [2, 4, 3, 2, 2, 3, 2, 2]
        for i in range(0,8):#8
            kind_url="http://www.qingzhoumuseum.cn/cp/"+str(kind[i])
            # print('#' * 40 + '1')
            # print(kind[i])
            # print(kind_url)
            # print('#' * 40 + '2')
            page=["index.html","index_1.html","index_2.html","index_3.html","index_4.html"]
            for j in range(0,int(page_num[i])):
                page_url=kind_url+page[j]
                # print('#' * 40 + '1')
                # print(page_url)
                # print('#' * 40 + '2')
                yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True,meta={"kind":kind_url})
        pass
    def parse_page(self,response):
        kind=response.meta['kind']
        tridvs=response.xpath("//div[3]/table/tbody//tbody//tbody//tbody")
        #print(tridvs)
        for tridv in tridvs:
            info_url=tridv.xpath(".//tr[2]//a/@href").get()
            col_name=tridv.xpath(".//tr[2]//a//text()").get()
            col_picture=tridv.xpath(".//tr[1]//img/@src").get()

            if not info_url:
                continue
            else:
                info_url=str(info_url)
                info_url=info_url[2:]
                info_url=kind+info_url
                col_picture=col_picture[2:]
                col_picture=kind+col_picture
                # print('#' * 40 + '1')
                # print(info_url)
                # print(col_name)
                # print(col_picture)
                # print('#' * 40 + '2')
                yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print('#' * 40 + '2')
        col_info=response.xpath("//div[2]/table/tbody//div[@class='TRS_Editor']//text()").getall()
        col_info="".join(col_info).strip().replace("\n","").replace("\xa0","").replace(" ","")
        print('#' * 40 + '1')
        print(col_name)
        print(col_picture)
        print(col_info)
        print('#' * 40 + '2')
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era='不详',
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
        pass

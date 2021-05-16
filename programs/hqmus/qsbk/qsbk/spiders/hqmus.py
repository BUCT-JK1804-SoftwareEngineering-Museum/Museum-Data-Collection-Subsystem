import scrapy
from ..items import QsbkItem

class HqmusSpider(scrapy.Spider):
    name = 'hqmus'
    allowed_domains = ['http://www.hqbwy.org.cn']
    start_urls = ['http://www.hqbwy.org.cn/collection.html?childid=15569&epochid=&keyword=&page=1']
    col_id_num: int = 350410001
    mus_id_num: int = 3504
    mus_name_num = '华侨博物院'
    def parse(self, response):
        kind_page=[15569,15568,15567,15566,15565,15564]
        kind_num=[12,2,6,2,1,3]
        for i in range(0,6):#6
            kind_url="http://www.hqbwy.org.cn/collection.html?childid="+str(kind_page[i])+"&epochid=&keyword="
            # print('#' * 40 + '1')
            for j in range(1,kind_num[i]+1):
                page_url=kind_url+"&page="+str(j)
                # print(page_url)
                yield scrapy.Request(page_url,callback=self.parse_page,dont_filter=True)
            # print('#' * 40 + '2')
            # print('#' * 40 + '1')
            # print(kind_url)
            # print(kind_num[i])
            # print('#' * 40 + '2')
        pass
    def parse_page(self,response):
        hqdivs=response.xpath("//div[@class='collect-main']/ul/li")
        for hqdiv in hqdivs:
            col_name=hqdiv.xpath(".//img/@alt").get()
            col_picture="http://www.hqbwy.org.cn"+hqdiv.xpath(".//img/@src").get()
            info_url=hqdiv.xpath(".//a/@href").get()
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print(info_url)
            # print('#' * 40 + '2')
            yield scrapy.Request(info_url,callback=self.parse_info,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
        pass
    def parse_info(self,resposne):
        col_name=resposne.meta['col_name']
        col_picture=resposne.meta['col_picture']
        col_info=resposne.xpath("//div[@class='peple-detail-intro']//p[@class='MsoNormal']//text()").getall()
        col_info="".join(col_info).strip().replace("\xa0","").replace("\n","").replace(" ","")
        col_era='见藏品名称'
        item = QsbkItem(col_id=self.col_id_num, mus_id=self.mus_id_num, col_name=col_name, col_era=col_era,
                        col_info=col_info, mus_name=self.mus_name_num, col_picture=col_picture)
        self.col_id_num += 1
        yield item
        pass
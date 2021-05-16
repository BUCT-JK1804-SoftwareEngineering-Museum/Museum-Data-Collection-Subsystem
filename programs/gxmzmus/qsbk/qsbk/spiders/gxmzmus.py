import scrapy

from ..items import QsbkItem

class GxmzmusSpider(scrapy.Spider):
    name = 'gxmzmus'
    allowed_domains = ['http://www.amgx.org']
    start_urls = ['http://www.amgx.org/boutique.html']
    base_next_page="http://www.amgx.org/"
    base_col_picture="http://www.amgx.org"
    page_num=[4,8,3,3,1,1,1,1]

    col_id_num: int=450210001
    mus_id_num: int=4502
    mus_name_num='广西民族博物馆'
    def parse(self, response):
        pagedivs=response.xpath("//div[@class='mbinnerla']//ul[@class='mbinnerl02']//li[last()-1]//dl[@id='menu5']/dd")
        page_num_test=1
        for pagediv in pagedivs:
            page_url=pagediv.xpath(".//a/@href").get()
            if len(page_url)>25:
                page_url=str(page_url)
            else:
                page_url=self.base_next_page+str(page_url)
            yield scrapy.Request(page_url,callback=self.parse_kind,dont_filter=True,meta={"page_url":page_url,"now_page_num":self.page_num[page_num_test-1]})
            #break
            page_num_test+=1
        pass
    def parse_kind(self,response):
        kind_url=response.meta['page_url']
        now_page_num = response.meta['now_page_num']
        for i in range(1,now_page_num+1):
            url=kind_url+"&page="+str(i)
            # print('#' * 40 + '1')
            # print(url)
            # print('#' * 40 + '2')
            yield scrapy.Request(url,callback=self.parse_page,dont_filter=True)

    def parse_page(self,response):
        gxdivs=response.xpath("//div[@class='videoli']/dl")
        for gxdiv in gxdivs:
            col_name=gxdiv.xpath(".//div[@class='videocover']/a/@title").get()
            col_picture=gxdiv.xpath(".//div[@class='videocover']//img/@src").get()
            col_picture=self.base_col_picture+str(col_picture)
            info_url=gxdiv.xpath(".//div[@class='videocover']/a/@href").get()
            yield scrapy.Request(self.base_next_page+str(info_url),callback=self.parse_info,dont_filter=True,meta={"col_name":col_name,"col_picture":col_picture})
            # print('#' * 40 + '1')
            # print(col_name)
            # print(col_picture)
            # print('#' * 40 + '2')
        pass
    def parse_info(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        info_xpath=response.xpath("//div[@class='mbdetial']//table//tr[last()]/td")
        #print(info_xpath)
        col_info=info_xpath.xpath(".//tr[last()]//text()").getall()
        col_info="".join(col_info).strip()
        col_info=str(col_info).replace("\xa0","").replace(" ","").replace("\r","").replace("\n","").replace("\t","").replace("\u2003","")
        col_era=info_xpath.xpath(".//tr[1]//td[last()]/text()").get()
        # print('#' * 40 + '1')
        # print(col_name)
        # print(col_picture)
        # print(col_era)
        # print(col_info)
        # print('#' * 40 + '2')
        item=QsbkItem(col_id=self.col_id_num,mus_id=self.mus_id_num,col_name=col_name,col_era=col_era,
                      col_info=col_info,mus_name=self.mus_name_num,col_picture=col_picture)
        self.col_id_num+=1
        yield item
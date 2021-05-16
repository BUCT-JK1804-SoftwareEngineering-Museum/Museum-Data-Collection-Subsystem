import scrapy
from ..items import SdbwgItem


class Sdspider2Spider(scrapy.Spider):
    name = 'sdspider2'
    allowed_domains = ['http://www.capitalmuseum.org.cn/']
    start_urls = ['http://www.capitalmuseum.org.cn/jpdc/tcq.htm']
    base_url = "http://www.capitalmuseum.org.cn/jpdc/"
    x = 2

    mus_name_num = '首都博物馆'
    id_num = 51
    mus_ida = 1107
    def parse(self, response):

        i = 2
        j = 7

        for i in range(0,j):
            qtqs = response.xpath("//table[@id='__2']/tr[2]/td/table/tr["+str(i)+"]/td/table")
            # its = response.xpath(".//td")
            for qtq in qtqs:
                #爬取名字和图片地址
                name = qtq.xpath(".//a[@class='blan']//text()").get()
                img_url = qtq.xpath(".//td[@height='21']/a/@href").get()
                imgweb = qtq.xpath(".//tr[1]/td/a/@href").get()
                # print('#' * 40)
                # print(name)
                # print(img_url)
                # print('#' * 40)
                i += 2
                yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,meta={"name":name,
                                                                                                          "imgweb":imgweb})

        #设置“下一页”
        next_url = self.base_url+"tcq_"+str(self.x)+".htm"
        #测试网络跳转情况
        self.x += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        if self.x>31:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = self.base_url + response.meta["imgweb"]
        # image = response.xpath("//img/@src").get()
        # image = self.base_url + image
        introduction = response.xpath("//td[@class='wcontent']/table/tr[4]/td[2]/table/tr[2]/td/p[2]/text()").getall()
        introduction= "".join(introduction).strip()
        era = response.xpath("//td[@class='wcontent']/table/tr[4]/td[2]/table/tr[2]/td/p[1]/text()").getall()
        era = "".join(era).strip()
        item=SdbwgItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item
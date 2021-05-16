import scrapy
from ..items import XhmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['https://www.gznywmuseum.org/']
    start_urls = ['https://www.gznywmuseum.org/csnyzc/index.jhtml']
    base_url = "https://www.gznywmuseum.org"

    i = 2
    mus_name_num = '西汉南越王博物馆'
    id_num = 1
    mus_ida = 4402

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='nav navbar-nav']/li[4]/ul/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + fur, callback=self.parse_page, dont_filter=True,
                                 meta = {"fur":fur} )

    def parse_page(self,response):
        zps = response.xpath("//div[@class='cz-list-content']//a")
        for zp in zps:
            name = zp.xpath(".//p//text()").get()
            durl = zp.xpath(".//@href").get()
            # print('#' * 40)
            # print(name)
            # print(durl)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + durl, callback=self.parse_detail, dont_filter=True,
                                 meta = {"name":name} )

        # 设置“下一页”
        a = response.meta["fur"]
        a = a[:-6]
        next_url = self.base_url + a + "_" + str(self.i) + ".jhtml"
        # 测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        b = response.xpath("count(//div[@style='display:inline-block;']/a)").get()
        if b == "1.0":
            c = response.xpath("//div[@style='display:inline-block;']/a[last()]//text()").get()
        else:
            c = response.xpath("//div[@style='display:inline-block;']/a[last()-1]//text()").get()

        c = int(c)
        # c = c+1
        # print('#' * 40)
        # print(b)
        # print(c)
        # print(type(c))
        # print('#' * 40)
        if self.i > c:
            self.i = 2
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse_page, dont_filter=True, meta = {"fur":response.meta["fur"]})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.xpath("//div[@class='zoompic']/img/@src").get()
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//div[@class='cz-list-detail-view-info-content']//text()").getall()
        introduction = "".join(introduction).strip()
        item =XhmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

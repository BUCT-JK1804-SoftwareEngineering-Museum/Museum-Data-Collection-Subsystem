import scrapy
from ..items import GxmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.gxmuseum.cn/']
    start_urls = ['http://www.gxmuseum.cn/a/antique/index.html']
    base_url = "http://www.gxmuseum.cn/"

    i = 2
    mus_name_num = '广西壮族自治区博物馆'
    id_num = 1
    mus_ida = 4501

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='d3']/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(self.base_url+fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + fur, callback=self.parse_page, dont_filter=True,
                                 meta = {"fur":fur} )

    def parse_page(self,response):
        zps = response.xpath("//div[@class='listbox']/ul/li")
        for zp in zps:
            name = zp.xpath(".//a[2]//text()").get()
            durl = zp.xpath(".//a[1]/@href").get()
            ima = zp.xpath(".//a[1]/img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(durl)
            # print(ima)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + durl, callback=self.parse_detail, dont_filter=True,
                                 meta = {"name":name, "image":ima} )
        #
        # 设置“下一页”
        a = response.meta["fur"]
        a = a[:-10]
        # 获得数字编号
        b = response.meta["fur"]
        b = b[10:]
        b = b[1:-11]

        next_url = self.base_url+a+"list_"+b+"_"+str(self.i)+".html"
        # 测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        #
        c = response.xpath("//ul[@class='pagelist']/li[last()-3]//text()").get()
        c = int(c)

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

        image = response.meta["image"]
        image = self.base_url + image
        era = response.xpath("//div[@class='neirong']/ul/li[2]/span[3]//text()").get()

        introduction = response.xpath("//div[@class='neirong']/p//text()").getall()
        introduction = "".join(introduction).strip()
        item = GxmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item
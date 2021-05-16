import scrapy
import copy
from ..items import HymusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.hylae.com/']
    start_urls = ['http://www.hylae.com/index.php?ac=article&at=list&tid=37']
    base_url = "http://www.hylae.com/"

    i = 2
    mus_name_num = '汉阳陵博物馆'
    id_num = 1
    mus_ida = 6104

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='zl-nav']/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(fur)
            # print('#' * 40)
            yield scrapy.Request(fur, callback=self.page, dont_filter=True,
                                 meta = {"fur":fur} )
    def page(self,response):
        fur = response.meta["fur"]
        b = response.xpath("//div[@id='pagination']/a[last()-1]//text()").get()

        if b==None: b = 1
        else: b = int (b)
        # print('#' * 40)
        # print(fur)
        # print(b)
        # print(type(b))
        # print('#' * 40)
        y = self.i
        yield scrapy.Request(fur, callback=self.parse_page, dont_filter=True,
                             meta={"fur": fur,"b":b,"y":y})

    def parse_page(self,response):
        zps = response.xpath("//div[@class='cangpin-pic']/ul/li")
        for zp in zps:
            name = zp.xpath(".//span[2]/a//text()").get()
            durl = zp.xpath(".//a/@href").get()
            ima = zp.xpath(".//a/img/@src").get()
            yield scrapy.Request(durl, callback=self.parse_detail, dont_filter=True,
                                 meta = {"name":name, "image":ima} )

        # 设置“下一页”
        a = response.meta["fur"]
        a = a[-2:]
        next_url = "http://www.hylae.com/index.php?page=" + str(self.i) + "&ac=article&at=list&tid=" + a
        # # 测试网络跳转情况
        j = self.i
        self.i += 1
        # print('#' * 40)
        # print(a)
        # print(next_url)
        c = response.meta["b"]
        # print(c)
        # print('#' * 40)
        # print('#' * 40)
        # print(c)
        # print(type(c))
        # print('#' * 40)
        if self.i > c+1:
            self.i = 2
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse_page, dont_filter=True,
                                 meta = {"fur":copy.deepcopy(response.meta["fur"]),
                                         "b":copy.deepcopy(response.meta["b"])})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//div[@class='list-right-box']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        item =HymusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

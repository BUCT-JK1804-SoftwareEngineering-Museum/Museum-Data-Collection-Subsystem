import scrapy
from ..items import XamusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.beilin-museum.com/']
    start_urls = ['http://www.beilin-museum.com/index.php?m=home&c=Lists&a=index&tid=72']
    base_url = "http://www.beilin-museum.com/"

    i = 2
    mus_name_num = '西安碑林博物馆'
    id_num = 1
    mus_ida = 6105

    #找到目录
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='piclist']/li")
        for qtq in qtqs:
            fur = qtq.xpath(".//a/@href").get()
            name = qtq.xpath(".//a/p/text()").get()
            ima = qtq.xpath(".//a/div/img/@src").get()
            # print('#' * 40)
            # print(fur)
            # print('#' * 40)
            yield scrapy.Request(self.base_url+fur,
                                 callback=self.parse_detail, dont_filter=True,
                                 meta = {"name":name, "image":ima} )

        # 设置“下一页”
        next_url = "http://www.beilin-museum.com/index.php?m=home&c=Lists&a=index&tid=72&page=" + str(self.i)
        # 测试网络跳转情况
        self.i += 1
        print('#' * 40)
        print(next_url)
        print('#' * 40)
        if self.i > 16:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num

        image = response.meta["image"]
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//div[@class='p']//text()").getall()
        introduction = "".join(introduction).strip()
        introduction = introduction.replace("\n", "")
        introduction = introduction.replace("\t", "")
        introduction = introduction.replace("\xa0", "")
        item =XamusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

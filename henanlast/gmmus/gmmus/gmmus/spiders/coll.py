import scrapy
from ..items import GmmusItem

class CollSpider(scrapy.Spider):
    name = 'coll'
    allowed_domains = ['http://www.eywsqsfbwg.com/']
    start_urls = ['http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=lists&catid=15']
    base_url = "http://www.eywsqsfbwg.com/"

    i = 2
    mus_name_num = '鄂豫皖苏区首府革命博物馆'
    id_num = 1
    mus_ida = 4106

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='of']/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//p//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            ima = qtq.xpath(".//a/img/@src").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print(ima)
            # print('#' * 40)

            yield scrapy.Request(img_url, callback=self.parse_detail,dont_filter=True,
                                 meta={"name":name,"image":ima} )


        # 设置“下一页”
        j = self.i
        next_url = self.base_url+"index.php?m=content&c=index&a=lists&catid=15&page="+str(j)
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        if self.i>3:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)


    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//div[@class='newscon']//text()").getall()
        introduction = "".join(introduction).strip()
        item=GmmusItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item
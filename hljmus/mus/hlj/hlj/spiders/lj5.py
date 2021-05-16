import scrapy
from ..items import HljItem

class Lj5Spider(scrapy.Spider):
    name = 'lj5'
    allowed_domains = ['http://www.hljmuseum.com/']
    start_urls = ['http://www.hljmuseum.com/cpgz/cpxs/wxzl/']
    base_url = "http://www.hljmuseum.com/"
    i=2

    mus_name_num = '黑龙江省博物馆'
    id_num = 27
    mus_ida = 2304
    def parse(self, response):
        qtqs = response.xpath("//ul[@class='titlepic05 huis']/div")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//span//text()").get()
            img_url = qtq.xpath(".//img/@src").get()
            fur_url = qtq.xpath(".//a/@href").get()

            yield scrapy.Request(self.base_url+fur_url, callback=self.parse_detail,
                                 dont_filter=True,meta={"name":name, "image":img_url})

            #yield item

        #设置“下一页”
        # j = self.i
        # next_url = self.base_url+"/dzzp/qtq/index_"+str(j)+".html"
        #
        # #测试网络跳转情况
        # self.i += 1
        #
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        # if self.i>9:
        #     return
        # else:
        #     yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)
    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        # image = response.xpath("//img/@src").get()
        image = response.meta["image"]
        era= ""
        # introduction = ""
        introduction = response.xpath("//div[@class='duanluo']//text()").getall()
        introduction = "".join(introduction).strip()

        item=HljItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item

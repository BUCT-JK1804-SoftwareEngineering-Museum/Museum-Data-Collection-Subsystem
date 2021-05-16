import scrapy
from ..items import ExmItem

class Ex2Spider(scrapy.Spider):
    name = 'ex2'
    allowed_domains = ['https://www.dlmodernmuseum.com/']
    start_urls = ['http://www.dlmodernmuseum.com/exhibition/']
    base_url = "https://www.dlmodernmuseum.com"
    id_num = 1
    mus_ida = 2106
    mus_name_num = '大连现代博物馆'
    timmme = '常年开放'
    i = 2

    def parse(self, response):
        qtqs = response.xpath("//div[@class='showlist contrightlist']/ul/li")
        for qtq in qtqs:
            # 爬取名字和图片地址
            name = qtq.xpath(".//div[@class='showimg w340 h510']/img/@alt").get()
            img_url = qtq.xpath(".//img/@src").get()
            img_url = self.base_url + img_url
            fur_url = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            era = qtq.xpath(".//a/div/div/p//text()").get()
            # era = "".join(era).strip()
            # print('#' * 40)
            # print(era)
            # print('#' * 40)
            yield scrapy.Request(fur_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name, "image":img_url, "era":era})

            # yield item
        #
        # 设置“下一页”
        # j = self.i
        # next_url = self.fur_url + str(j) + ".html"
        #
        # # 测试网络跳转情况
        # self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        # if self.i > 8:
        #     return
        # else:
        #     yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)


    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 20000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        time = response.meta["era"]
        # info = response.xpath("//div[@class='showlist contrightlist']/p[last]//text()").getall()
        info = response.xpath("//div[@class='showlist contrightlist']//text()").getall()
        info = "".join(info).strip()

        # print('#' * 40)
        # print(info)
        # print('#' * 40)
        item=ExmItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1

        yield item
import scrapy
from ..items import DlmusItem

class Mus1Spider(scrapy.Spider):
    name = 'mus1'
    allowed_domains = ['https://www.dlmodernmuseum.com/']
    start_urls = ['https://www.dlmodernmuseum.com/collection/1.html']
    base_url = "https://www.dlmodernmuseum.com/"
    fur_url = "https://www.dlmodernmuseum.com/collection/"
    i = 2
    mus_name_num = '大连现代博物馆'
    id_num = 1
    mus_ida = 2106

    def parse(self, response):
        qtqs = response.xpath("//div[@class='showlist contrightlist']/ul/li")
        for qtq in qtqs:
            # 爬取名字和图片地址
            name = qtq.xpath(".//div[@class='showtitle2']//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            yield scrapy.Request(img_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name})

            # yield item
        #
        # 设置“下一页”
        j = self.i
        next_url = self.fur_url + str(j) + ".html"

        # 测试网络跳转情况
        self.i += 1
        # print('#' * 40)
        # print(next_url)
        # print('#' * 40)
        if self.i > 8:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//div[@class='showlist contrightlist']/p[1]/img/@src").get()
        # flag_ima = response.xpath("//div[@class='infocontent']//img/@border").get()
        # if flag_ima == "0":
        #     image = ima
        # else:
        image = self.base_url + image

        # print('#' * 40)
        # print(ima)
        # print(flag_ima)
        # print('#' * 40)

        era = "null"
        introduction = response.xpath("//div[@class='showlist contrightlist']/p[last()]//text()").getall()
        introduction = "".join(introduction).strip()
        item = DlmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

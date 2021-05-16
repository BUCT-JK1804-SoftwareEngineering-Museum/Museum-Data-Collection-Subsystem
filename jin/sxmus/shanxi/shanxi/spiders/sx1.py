import scrapy
from ..items import ShanxiItem


class Sx1Spider(scrapy.Spider):
    name = 'sx1'
    allowed_domains = ['http://www.shanximuseum.com/']
    start_urls = ['http://www.shanximuseum.com/sx/collection/classic.html']

    mus_name_num = '宝鸡青铜器博物馆'
    id_num = 1
    mus_ida = 6108

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='clearfix']/li")
        for qtq in qtqs:
            # 爬取名字和图片地址
            name = qtq.xpath(
                ".//h2[@class='mar-t10 mar-b10 pad-l5 pad-r5 c-333 t-a-c f-siz16 f-wei-b ellipsis']//text()").get()
            img_url = qtq.xpath(".//a[@class='pos-a w100 h100 dis-b t l']/@href").get()

            yield scrapy.Request(self.base_url + img_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name})

            # yield item

        # 设置“下一页”
        j = self.i
        next_url = self.base_url + "/dzzp/qtq/index_" + str(j) + ".html"

        # 测试网络跳转情况
        self.i += 1

        print('#' * 40)
        print(next_url)
        print('#' * 40)
        if self.i > 9:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//img/@src").get()
        image = self.base_url + image
        era = response.xpath("//div[@class='mar-t20 pad-b25 article']/p[1]/text()").getall()
        # era= "".join(era).strip()
        introduction = response.xpath("//div[@class='mar-t20 pad-b25 article']/p[last()]//text()").getall()
        introduction = "".join(introduction).strip()
        item = BjmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

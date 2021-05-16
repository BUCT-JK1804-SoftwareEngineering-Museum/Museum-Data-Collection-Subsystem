import scrapy

from ..items import ExmusItem
class Ex1Spider(scrapy.Spider):
    name = 'ex1'
    allowed_domains = ['http://www.kmycjng.com/']
    start_urls = ['http://www.kmycjng.com/list?cid=24']
    fur_url = "http://www.kmycjng.com/list?pageid="
    base_url = "http://www.kmycjng.com/"
    i = 2
    mus_name_num = '抗美援朝纪念馆'
    id_num = 1
    mus_ida = 2103
    timmme = '常年开放'

    def parse(self, response):
        qtqs = response.xpath("//div[@class='sy_jccl']/ul/li")
        for qtq in qtqs:
            # 爬取名字和图片地址
            name = qtq.xpath(".//div[@class='sy_title']//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + img_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name})
        # 设置“下一页”
        j = self.i
        next_url = self.fur_url + str(j) + "&cid=24"

        # 测试网络跳转情况
        self.i += 1
        print('#' * 40)
        print(next_url)
        print('#' * 40)
        if self.i > 4:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//div[@class='infocontent']//img/@src").get()
        image = self.base_url + image
        time = self.timmme
        info = "null"
        item=ExmusItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1

        yield item
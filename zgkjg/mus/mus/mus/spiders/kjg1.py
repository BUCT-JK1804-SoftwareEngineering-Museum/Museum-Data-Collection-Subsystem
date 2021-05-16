import scrapy
from ..items import MusItem


class Kjg1Spider(scrapy.Spider):
    name = 'kjg1'
    allowed_domains = ['https://cstm.cdstm.cn/']
    start_urls = ['https://cstm.cdstm.cn/cszl/cszljs/']
    base_url = "https://cstm.cdstm.cn/cszl/cszljs/"

    i = 1
    mus_name_num = '中国科学技术馆'
    id_num = 1
    mus_ida = 1102
    timee = "常年开放"

    def parse(self, response):
        qtqs = response.xpath("//ul[@class='fen-menu2-list']/li")
        tus = response.xpath("//div[@class='cszl-fent']/div")
        for qtq,tu in zip(qtqs[1:],tus):
            # 爬取名字和图片地址
            name = qtq.xpath(".//a/text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            ima = tu.xpath(".//a/img/@src").get()
            #
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print(ima)
            # print('#' * 40)
            yield scrapy.Request(self.base_url + img_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"name": name, "image":ima, "url":img_url})


    def parse_detail(self,response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.meta["image"]
        time = self.timee
        # info = response.xpath("//div[@class='showlist contrightlist']/p[last]//text()").getall()
        # print('#' * 40)
        # print(response.meta["url"])
        # print('#' * 40)
        if(response.meta["url"] == "../../kxly/"):
            info = response.xpath("//div[@class='main-wapper main-wapper-kxly Bgimg-fen-kxly']").get()
            print('#' * 40)
            print(info)
            print('#' * 40)
            # info = response.xpath("//div[@class='']//text()").getall()

        else:
            info = response.xpath("//div[@class='TRS_Editor']//text()").getall()

            info = "".join(info).strip()

        # print('#' * 40)
        # print(info)
        # print('#' * 40)
        item=MusItem(name=name,id=id,mus_id=mus_id,mus_name=mus_name,image=image,
                      time=time,info=info)
        self.id_num += 1

        yield item


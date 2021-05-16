import scrapy
from ..items import JunboItem

class Jbspider3Spider(scrapy.Spider):
    name = 'jbspider3'
    allowed_domains = ['www.jb.mil.cn/']
    start_urls = ['http://www.jb.mil.cn/was/web/search?token=14.1499419140318.94&channelid=287610&perpage=200']
    shit_url = "http://www.jb.mil.cn/gcww/wwjs_new/gjdww/201707/"

    id_num = 109
    mus_ida = 1104
    mus_name_num = '中国人民革命军事博物馆'

    def parse(self, response):
        # lists = response.xpath("//div[@class='relicAppLeft']ul/li")
        tdgms = response.xpath("//div[@class='raAppList']/ul/li")
        # print('#' * 40)
        # print(gjds)
        # print('#' * 40)
        for tdgm in tdgms:
            # 爬取名字和图片地址
            name = tdgm.xpath(".//span/text()").get()
            # img = gjd.xpath(".//img/@src").getall()
            # img = gjd.xpath(".//script[2]").get()
            img_url = tdgm.xpath(".//a/@href").get()
            yield scrapy.Request(img_url, callback=self.parse_detail, dont_filter=True, meta={"name": name})

    def parse_detail(self, response):
        name = response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//img/@oldsrc").get()
        image = self.shit_url + image
        era = response.xpath("//div[@class='TRS_Editor']/p[2]//text()").getall()
        era = "".join(era).strip()
        introduction = response.xpath("//div[@class='TRS_Editor']/p[3]//text()").getall()
        introduction = "".join(introduction).strip()

        item = JunboItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
                         introduction=introduction)
        self.id_num += 1
        yield item

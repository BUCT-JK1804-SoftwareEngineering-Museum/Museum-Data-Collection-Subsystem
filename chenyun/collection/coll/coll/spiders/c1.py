import scrapy
from ..items import CollItem

class C1Spider(scrapy.Spider):
    name = 'c1'
    allowed_domains = ['http://www.cyjng.net/']
    start_urls = ['http://www.cyjng.net/Default.aspx?tabid=62&language=zh-CN']
    base_url = "http://www.cyjng.net/"

    i=2
    mus_name_num = '陈云纪念馆'
    id_num = 1
    mus_ida = 3105
    era = "null"
    def parse(self, response):
        qtqs = response.xpath("//table[@class='ArticleList']/tr")
        for qtq in qtqs:

            # zps = qtq.xpath("//table[@width='100%']")

            zps = qtq.xpath("./td")
            # print('#' * 40)
            # print(zps)
            # print('#' * 40)
            for zp in zps:
                #爬取名字和图片地址
                name = zp.xpath(".//a[@class='Normal']//text()").get()
                img_url = zp.xpath(".//a[@class='Normal']/@href").get()
                # print('#' * 40)
                # print(name)
                # print(img_url)
                # print('#' * 40)
                if name != None:
                    yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,meta={"name":name})

            #yield item

        # #设置“下一页”
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
        image = response.xpath("//td[@align='center']/img/@src").get()
        image = self.base_url + image
        era = self.era
        introduction = response.xpath("//span[@class='normal']/p//text()").getall()
        introduction = "".join(introduction).strip()
        item=CollItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item

import scrapy
from ..items import ZzmusItem

class ZpSpider(scrapy.Spider):
    name = 'zp'
    allowed_domains = ['http://www.hnzzmuseum.com/']
    start_urls = ['http://www.hnzzmuseum.com/collection5_list.html']
    base_url = "http://www.hnzzmuseum.com/"

    i = 6
    mus_name_num = '郑州博物馆'
    id_num = 1
    mus_ida = 4102

    def parse(self, response):
        qtqs = response.xpath("//div[@class='bd']/ul/li")
        for qtq in qtqs:
            #爬取名字和图片地址
            name = qtq.xpath(".//span[@class='bd_con_t']//text()").get()
            img_url = qtq.xpath(".//a/@href").get()
            # print('#' * 40)
            # print(name)
            # print(img_url)
            # print('#' * 40)

            yield scrapy.Request(self.base_url+img_url, callback=self.parse_detail,dont_filter=True,meta={"name":name})


        #设置“下一页”
        j = self.i
        next_url = self.base_url+"collection"+str(j)+"_list.html"

        #测试网络跳转情况
        self.i += 1
        print('#' * 40)
        print(next_url)
        print('#' * 40)
        if self.i>9:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        name=response.meta["name"]
        id = str(self.id_num + self.mus_ida * 100000 + 10000)
        mus_id = str(self.mus_ida)
        mus_name = self.mus_name_num
        image = response.xpath("//div[@class='p_solid']/ul/li/img/@src").get()
        image = self.base_url + image
        era = "见简介"
        introduction = response.xpath("//p[@style='text-indent:2em;']//text()").getall()
        introduction = "".join(introduction).strip()
        item=ZzmusItem(id=id,mus_id=mus_id,name=name,mus_name=mus_name,image=image,era=era,introduction=introduction)
        self.id_num += 1
        yield item
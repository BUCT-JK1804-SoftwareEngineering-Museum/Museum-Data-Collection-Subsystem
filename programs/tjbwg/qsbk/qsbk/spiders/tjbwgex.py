import scrapy

from ..items import DtxsexItem

class TjbwgexSpider(scrapy.Spider):
    name = 'tjbwgex'
    allowed_domains = ['https://www.tjbwg.com']
    start_urls = ['https://www.tjbwg.com/cn/ExhibitionList.aspx?TypeId=10939']
    base_domin= "https://www.tjbwg.com/cn/"
    exh_id_num: int = 120110006
    mus_id_num: int = 1201
    mus_name_num = '天津博物馆'
    def parse(self, response):
        divs=response.xpath("//div[@class='exhList2']/ul[@class='clearfix']/li")
        for div in divs:
            exh_id = self.exh_id_num
            self.exh_id_num += 1
            mus_id = self.mus_id_num
            mus_name = self.mus_name_num
            exh_name = div.xpath(".//div[@class='text']/h3//text()").get().strip()
            exh_picture = div.xpath(".//div[@class='img']/img/@src").get().strip()
            exh_picture = self.base_domin + exh_picture
            img_url = div.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_domin + img_url, callback=self.parse_detail, dont_filter=True,meta={"exh_id": exh_id, "exh_name": exh_name, "mus_id": mus_id, "mus_name": mus_name,"exh_picture": exh_picture})
        return
    def parse_detail(self, response):
        exh_id = response.meta["exh_id"]
        exh_name=response.meta["exh_name"]
        mus_id=response.meta["mus_id"]
        mus_name=response.meta["mus_name"]
        exh_picture = response.meta["exh_picture"]
        exh_time=response.xpath("//div[@class='text']/p[1]//text()").get().strip()
        exh_info = response.xpath("//div[@class='exhUs_r']//text()").getall()
        exh_info = "".join(exh_info).strip()
        item = DtxsexItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_picture=exh_picture, exh_time=exh_time, exh_info=exh_info)
        yield item
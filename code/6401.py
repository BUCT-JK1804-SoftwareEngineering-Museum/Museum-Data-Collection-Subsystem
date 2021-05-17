import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '6401'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://nxgybwg.com/e/action/ListInfo/index.php?page=0&classid=17']
    # 用于数据解析，相应对象 response
# 'http://nxgybwg.com/e/action/ShowInfo.php?classid=47&id=346'

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div/div[1]/h1/text()').extract()[0]
        mus_name='固原博物馆'
        col_picture=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div/div[2]/div/p[1]/img/@src').extract()[0]
        if len(col_picture)<78:
            col_picture='http://nxgybwg.com'+col_picture
        col_infod=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div/div[2]/div//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=6401
        item = Item()
        item['mus_name'] = mus_name
        item['mus_id'] = mus_id
        item['col_id'] = response.meta['col_id']
        item['col_name'] = col_name
        item['col_info'] = col_info
        item['col_picture'] = col_picture
        item['col_era'] = 'null'
        yield item
        print("正在爬取藏品 " + item['col_name'] + " ing")
        return

    # 藏品列表
    def parse_cols(self, response):
        li=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div[2]/ul')
        for i in li:
            new_url=i.xpath('.//a/@href').extract()
            for j in new_url:
                cp_url='http://nxgybwg.com'+j
                yield scrapy.Request(cp_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '固原博物馆'
        item['mus_id'] = 6401
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]//div[@class="read_header"]/h1/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('////*[@id="body_wrap"]/div/div[2]/div[2]/div/div[2]/div//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div/div[2]//img/@src').extract()
        if len(exh_picture):
            exh_picture=exh_picture[0]
            if len(exh_picture)<60:
                exh_picture='http://nxgybwg.com'+exh_picture
            else:
                pass
        else:
            exh_picture.append("null")
            exh_picture=exh_picture[0]
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="body_wrap"]/div/div[2]/div[2]/div[2]')
        for i in pro:
            news_url=i.xpath('./dl/dt//a/@href').extract()
            for j in news_url:
                zl_url='http://nxgybwg.com'+j
                if len(zl_url)<65:
                    yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
    #主函数
    def parse(self,response):
        col_id = 640100001
        for i in range(0,4):
            col_id+=1000
            col_url='http://nxgybwg.com/e/action/ListInfo/index.php?page=%s'%(str(i))+'&classid=17'
            yield scrapy.Request(col_url,callback=self.parse_cols,meta={'col_id':col_id})

        exh_id=640100001
        for t in range(0,6):
            exh_id+=1000
            exh_url='http://nxgybwg.com/e/action/ListInfo/index.php?page=%s'%(str(t))+'&classid=12'
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})
        return
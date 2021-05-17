import json

import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3798'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.qdyzyzmuseum.com/']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//h3[@class="h3title"]/text()').extract()[0]

        col_era='null'
        mus_name='青岛山炮台遗址展览馆'
        col_picture='http://www.qdyzyzmuseum.com'+response.xpath('/html/body/div[5]/div/div/div[2]/div[2]/div/p/img/@src').extract()[0].strip('.')
        col_info="null"
        mus_id=3798
        item =Item()
        item['mus_name']=mus_name
        item['mus_id']=mus_id
        item['col_id']=response.meta['col_id']
        item['col_name']=col_name
        item['col_info']=col_info
        item['col_picture']=col_picture
        item['col_era']='null'
        yield item
        print("正在爬取藏品 "+item['col_name']+" ing")
        return

    # 藏品列表
    def parse_cols(self, response):
        root=response.xpath('/html/body/div[5]/div/div/div[2]')
        for i in root:
            url=i.xpath('./div/a/@href').extract()
            for j in url:
                new_url='http://www.qdyzyzmuseum.com'+j
                yield scrapy.Request(new_url,callback=self.parse_new,meta={'col_id': response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '古田会议纪念馆'
        item['mus_id'] = 3502
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="activity-name"]//text()').extract()[0]
        exh_name=''.join(exh_name).strip()
        exh_name="".join(exh_name).replace(' ','')
        exh_name=''.join(exh_name).replace('\n','')
        exh_name=''.join(exh_name).replace('\t','')
        exh_name=''.join(exh_name).replace('r','')
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="img-content"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        item['exh_info']=exh_info
        exh_picture="null"

        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList1(self,response):
        pro=response.xpath('//div[@class="tit_ul"]/ul')
        for i in pro:
            news_url=i.xpath('./li/p/a/@href').extract()
            for j in news_url:
                zl_url=j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return
    def parse_exlList2(self,response):
        pro=response.xpath('//div[@class="tit_ul"]/ul')
        for i in pro:
            news_url=i.xpath('./li/p/a/@href').extract()
            for j in news_url:
                zl_url=j
                print(zl_url)
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return
    #主函数
    def parse(self,response):
        # col_id = 379800001
        # col_id+=100
        # col_url='http://www.qdyzyzmuseum.com/Home/Diancang/index/cateid/46'
        # yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})


        # exh_id=350200001
        # for t in range(0,4):
        #     if t==0:
        #         exh_id+=100
        #         exh_url='http://www.gthyjng.com/shjy/xxjyhd/index.htm'
        #         yield scrapy.Request(exh_url, callback=self.parse_exlList1, meta={'exh_id': exh_id, 'url': exh_url})
        #     else:
        #         exh_id+=100
        #         exh_url='http://www.gthyjng.com/shjy/xxjyhd/index_%s'%str(t)+'.htm'
        #         yield scrapy.Request(exh_url,callback=self.parse_exlList2,meta={'exh_id':exh_id,'url':exh_url})

        return
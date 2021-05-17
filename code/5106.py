import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '5106'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.scmuseum.cn/list-1657-1.html']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="article-1"]/h1/text()').extract()[0]
        mus_name='四川博物院'
        col_picture='http://www.scmuseum.cn'+response.xpath('//*[@id="article-1"]/div[1]/img/@src').extract()[0]
        col_infod=response.xpath('//*[@id="article-1"]/div[3]//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=5106
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
        li=response.xpath('//*[@id="portfolio"]')
        for i in li:
            new_ulr=i.xpath('./div[@class="tile medium tscpbox"]//a/@href').extract()
            for j in new_ulr:
                yield scrapy.Request(j, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
                response.meta['col_id'] += 1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '四川博物院'
        item['mus_id'] = 5106
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="article-1"]/h1/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="MyContent"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture=response.xpath('//*[@id="MyContent"]//img/@src').extract()
        if len(exh_picture)<1:
            exh_picture='null'
        else:
            exh_picture=exh_picture[0]
            if len(exh_picture)<50:
                exh_picture='http://www.scmuseum.cn/'+exh_picture
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        #
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="zhanlan-left"]')
        for i in pro:
            news_url=i.xpath('./div[@class="zhanlanlist"]/a/@href').extract()
            for j in news_url:
                zl_url=j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1

    # 主函数
    def parse(self,response):
        # col_id = 510600001
        # for i in range(1,25):
        #     col_url='http://www.scmuseum.cn/list-1657-%s'%str(i)+'.html'
        #     yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})
        #     col_id+=100

        exh_id=510600001
        for t in range(1,7):
                exh_url='http://www.scmuseum.cn/list-1675-%s'%str(t)+'.html'
                yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})
                exh_id += 100
        return
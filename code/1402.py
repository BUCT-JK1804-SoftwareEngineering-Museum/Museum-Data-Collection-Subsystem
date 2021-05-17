import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1402'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['https://www.tjnhm.com/index.php?p=kxyj&lanmu=4&c_id=16&page=1']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):

        col_name=response.xpath('//*[@id="wrap"]/div[2]/div[1]/text()').extract()[0]
        mus_name='中国煤炭博物馆'
        col_picture=response.xpath('//*[@id="wrap"]/div[2]/div[5]/div[1]/div/div/img/@src').extract()[0]
        print(col_picture)
        col_info="null"
        # col_info="".join(col_infod).strip()
        # col_info=''.join(col_info).replace(' ','')
        # col_info=''.join(col_info).replace('\r','')
        # col_info = ''.join(col_info).replace('\t', '')
        # col_info = ''.join(col_info).replace('\n', '')
        # col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=1402
        item =Item()
        item['mus_name']=mus_name
        item['mus_id']=mus_id
        item['col_id']=response.meta['col_id']
        item['col_name']=col_name
        item['col_info']=col_info
        item['col_picture']=col_picture
        item['col_era']='null'
        print(response.meta['col_id'])
        yield item
        print("正在爬取藏品 "+item['col_name']+" ing")
        return

    def parse_col(self,response):
        li=response.xpath('//*[@id="wrap"]/div[2]/div[2]/ul')
        for i in li:
            url=i.xpath('./li/div[1]/a/@href').extract()
            for j in url:
                yield scrapy.Request(j,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '中国煤炭博物馆'
        item['mus_id'] = 1402
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//div[@id="xw_title"]//text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="xw_content"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        item['exh_info']=exh_info
        # yy="https://www.tjnhm.com/"
        exh_picture=response.xpath('///*[@id="xw_content"]//img/@src').extract()
        if len(exh_picture)==0:
            exh_picture='null'
        else:
            exh_picture='http://www.coalmus.org.cn/'+exh_picture[0]
        #
        item['exh_picture'] = exh_picture
        item['exh_time']='null'
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="LB"]/ul')
        for i in pro:
            news_url=i.xpath('./li/p/a/@href').extract()
            for j in news_url:
                zl_url=j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
    # 主函数
    def parse(self,response):
        col_id = 140200001
        col_url = 'http://www.coalmus.org.cn/html/list_1562.html'
        yield scrapy.Request(col_url, callback=self.parse_col, meta={'col_id': col_id})
        col_id+=100

        col_url = 'http://www.coalmus.org.cn/html/list_1556.html'
        yield scrapy.Request(col_url, callback=self.parse_col, meta={'col_id': col_id})
        col_id += 100

        col_url = 'http://www.coalmus.org.cn/html/list_1557.html'
        yield scrapy.Request(col_url, callback=self.parse_col, meta={'col_id': col_id})
        col_id += 100

        col_url = 'http://www.coalmus.org.cn/html/list_1560.html'
        yield scrapy.Request(col_url, callback=self.parse_col, meta={'col_id': col_id})
        col_id += 100

        exh_id=140200001
        exh_id+=100
        exh_url='http://www.coalmus.org.cn/html/list_1659.html'
        yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        exh_id += 100
        exh_url = 'http://www.coalmus.org.cn/html/list_1659_1.html'
        yield scrapy.Request(exh_url, callback=self.parse_exlList, meta={'exh_id': exh_id, 'url': exh_url})

        return
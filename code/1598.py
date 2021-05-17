import json

import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1598'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.cfbwg.org.cn/chifengnet/list-5bb02c1c29d849f1a3b489c1509e174e.html?type=%E6%BC%86%E6%9C%A8%E5%99%A8']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//div[@class="main-title"]/h2/text()').extract()[0]
        mus_name='赤峰博物馆'
        col_picture='http://www.cfbwg.org.cn'+response.xpath('//div[@class="text"]//img/@src').extract()[0]
        col_info=response.xpath('/html/body/div[2]/div/div[2]/div[2]/table/tbody/tr[7]/td[2]/p//text()').extract()
        col_info="".join(col_info).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=1598
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
        root=json.loads(response.body)
        for root_url in root:
            url='http://www.cfbwg.org.cn/'+root_url['url']
            yield scrapy.Request(url, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
            response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '赤峰博物馆'
        item['mus_id'] = 1598
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[2]/div/div[2]/div[1]/h2/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[2]/div/div[2]/div[2]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture='http://www.cfbwg.org.cn'+response.xpath('/html/body/div[2]/div/div[2]/div[2]//img/@src')[0].extract()
        exh_era="null"
        item['exh_time'] = exh_era
        item['exh_picture']=exh_picture
        #
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        root = json.loads(response.body)
        for root_url in root:
            url = 'http://www.cfbwg.org.cn/' + root_url['url']
            yield scrapy.Request(url, callback=self.parse_exl, meta={'exh_id': response.meta['exh_id']})
            response.meta['exh_id'] += 1
        return


    # 主函数
    def parse(self,response):
        # col_id = 159800001
        # url='http://www.cfbwg.org.cn//chifengnet/newController/searchjizhen?type=%E6%BC%86%E6%9C%A8%E5%99%A8'
        # yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        # col_id+=100
        #
        # url1 = 'http://www.cfbwg.org.cn//chifengnet/newController/searchjizhen?type=%E6%B0%91%E6%97%8F%E6%96%87%E7%89%A9'
        # yield scrapy.Request(url1, callback=self.parse_cols, meta={'col_id': col_id})
        # col_id += 100
        #
        # url2 = 'http://www.cfbwg.org.cn//chifengnet/newController/searchjizhen?type=%E9%87%91%E9%93%B6%E5%99%A8'
        # yield scrapy.Request(url2, callback=self.parse_cols, meta={'col_id': col_id})
        # col_id += 100
        #
        # url2 = 'http://www.cfbwg.org.cn//chifengnet/newController/searchjizhen?type=%E9%99%B6%E5%99%A8'
        # yield scrapy.Request(url2, callback=self.parse_cols, meta={'col_id': col_id})
        # col_id += 100

        exh_id=159800001
        url='http://www.cfbwg.org.cn//chifengnet/newController/searchzhanlanhuigu?times=&name='
        yield scrapy.Request(url, callback=self.parse_exlList, meta={'exh_id': exh_id})
        return

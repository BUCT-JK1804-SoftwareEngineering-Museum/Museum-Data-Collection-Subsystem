import json

import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '5001'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://3gmuseum.cn/']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[7]/div[3]/div[3]/div[2]/h2/text()').extract()[0]
        mus_name='重庆红岩革命历史博物馆'
        col_picture='https://www.hongyan.info/'+response.xpath('//div[@class="collection-content-pic"]//img/@src').extract()[0]
        col_infod=response.xpath('/html/body/div[7]/div[3]/div[3]/div[2]//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=5002
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
        j=json.loads(response.body)['list']
        for i in j:
            col_name=i['subject']
            col_info=i['contents']
            col_picture=['thumbnailimg']
            col_info = "".join(col_info).strip()
            col_info = ''.join(col_info).replace(' ', '')
            col_info = ''.join(col_info).replace('\r', '')
            col_info = ''.join(col_info).replace('\t', '')
            col_info = ''.join(col_info).replace('\n', '')
            col_info = col_info.replace("\u3000", "").replace("\xa0", "")
            mus_id = 5001
            item = Item()
            item['mus_name'] ='重庆三峡博物馆'
            item['mus_id'] = mus_id
            item['col_id'] = response.meta['col_id']
            item['col_name'] = col_name
            item['col_info'] = col_info
            item['col_picture'] = col_picture
            item['col_era'] = 'null'
            yield item
            print("正在爬取藏品 " + item['col_name'] + " ing")
            response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '天津自然博物馆'
        item['mus_id'] = 5002
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="aboutus_text"]/h1[1]/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//div[@id="aboutus_text"]/p//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        item['exh_info']=exh_info
        yy="https://www.tjnhm.com/"
        exh_picture=response.xpath('//*[@id="aboutus_text"]//p//img/@src')[0].extract()
        if len(exh_picture)<60:
            exh_picture=yy+exh_picture
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture

        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        j = json.loads(response.body)['list']
        for i in j:
            exh_name = i['subject']
            exh_info = i['contents']
            exh_picture = ['thumbnailimg']
            exh_info = "".join(exh_info).strip()
            exh_info = ''.join(exh_info).replace(' ', '')
            exh_info = ''.join(exh_info).replace('\r', '')
            exh_info = ''.join(exh_info).replace('\t', '')
            exh_info = ''.join(exh_info).replace('\n', '')
            exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
            mus_id = 5001
            item = Item()
            item['col_id']=''
            item['mus_name'] = '重庆三峡博物馆'
            item['mus_id'] = mus_id
            item['exh_id'] = response.meta['exh_id']
            item['exh_name'] = exh_name
            item['exh_info'] = exh_info
            item['exh_picture'] = exh_picture
            item['exh_time'] = 'null'
            yield item
            print("正在爬取藏品 " + item['exh_name'] + " ing")
            response.meta['exh_id'] += 1
        return

    # 主函数
    def parse(self,response):
        # col_id = 500200001
        # for i in range(1,7):
        #     col_id += 100
        #     data={
        #        "pageNumber":str(i),
        #         "pageSize":str(8),
        #         "itemno":'2c8481ec5bd16b52015bd18228ea0000'
        #     }
        #     url='http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url,callback=self.parse_cols,formdata=data,meta={'col_id': col_id})
        #     col_id+=100
        #
        # for i in range(1,8):
        #     col_id += 100
        #     data={
        #        "pageNumber":str(i),
        #         "pageSize":str(8),
        #         "itemno":'2c8481ec5bd16b52015bd184f31a0004'
        #     }
        #     url='http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url,callback=self.parse_cols,formdata=data,meta={'col_id': col_id})
        #     col_id+=100
        # for i in range(1,7):
        #     col_id += 100
        #     data={
        #        "pageNumber":str(i),
        #         "pageSize":str(8),
        #         "itemno":'2c8481ec5bd16b52015bd18419210002'
        #     }
        #     url='http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url,callback=self.parse_cols,formdata=data,meta={'col_id': col_id})
        #     col_id+=100
        # for i in range(1,4):
        #     col_id += 100
        #     data={
        #        "pageNumber":str(i),
        #         "pageSize":str(8),
        #         "itemno":'2c8481ec5bd16b52015bd18479f50003'
        #     }
        #     url='http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url,callback=self.parse_cols,formdata=data,meta={'col_id': col_id})
        #     col_id+=100
        # for i in range(1, 7):
        #     col_id += 100
        #     data = {
        #         "pageNumber": str(i),
        #         "pageSize": str(8),
        #         "itemno": '2c8481ec5bd16b52015bd18389510001'
        #     }
        #     url = 'http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url, callback=self.parse_cols, formdata=data, meta={'col_id': col_id})
        #     col_id += 100
        # for i in range(1, 5):
        #     col_id += 100
        #     data = {
        #         "pageNumber": str(i),
        #         "pageSize": str(8),
        #         "itemno": '2c8481ec5bd16b52015bd18561280005'
        #     }
        #     url = 'http://3gmuseum.cn/web/article/findArticleAndPage.do'
        #     yield scrapy.FormRequest(url, callback=self.parse_cols, formdata=data, meta={'col_id': col_id})
        #     col_id += 100

        exh_id=500100001
        for i in range(1, 5):
            exh_id += 100
            data = {
                "pageNumber": str(i),
                "pageSize": str(12),
                "itemno": '25434353'
            }
            url = 'http://3gmuseum.cn/web/exhibitionHallOften/conventionalExhibitionPage.do'
            yield scrapy.FormRequest(url, callback=self.parse_exlList, formdata=data, meta={'exh_id': exh_id})
            exh_id += 100
        return
    #

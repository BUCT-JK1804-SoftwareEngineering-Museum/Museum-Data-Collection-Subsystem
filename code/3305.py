import json

import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3305'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.hzmuseum.com/#/linzhanComponent?bread=%E5%BD%93%E5%89%8D%E5%B1%95%E8%A7%88']
    # 用于数据解析，相应对象 response


    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '杭州博物馆'
        item['mus_id'] = 3305
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.meta['js']['title']
        print(exh_name)
        # item['exh_name']=exh_name
        # exht_info=response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]//text()').extract()
        # exh_info=''.join(exht_info).strip()
        # exh_info="".join(exh_info).replace(' ','')
        # exh_info=''.join(exh_info).replace('\n','')
        # exh_info=''.join(exh_info).replace('\t','')
        # exh_info=''.join(exh_info).replace('r','')
        # exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        # item['exh_info']=exh_info
        # exh_picture='http://www.bjp.org.cn/'+response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div//img/@src')[0].extract()
        # item['exh_time'] = "null"
        # item['exh_picture']=exh_picture
        # # #
        # print("正在爬取展览 " + item['exh_name'] + " ing")
        # yield item
        return

    #展览列表
    def parse_exlList(self,response):
        js=json.loads(response.body)
        i=js['detail']
        url1='http://www.hzmuseum.com/#/'
        for j in i['list']:
            item = Item()
            item['col_id'] = ""
            item['mus_name'] = '杭州博物馆'
            item['mus_id'] = 3305
            item['exh_id'] = response.meta['exh_id']
            response.meta['exh_id'] += 1
            exh_name = j['title']
            item['exh_name'] = exh_name
            exh_info=j['jianjie']
            exh_info=''.join(exh_info).strip()
            exh_info="".join(exh_info).replace(' ','')
            exh_info=''.join(exh_info).replace('\n','')
            exh_info=''.join(exh_info).replace('\t','')
            exh_info=''.join(exh_info).replace('r','')
            exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
            item['exh_info']=exh_info
            exh_picture='http://www.hzmuseum.com'+j['fengmian']
            print(exh_picture)
            item['exh_time'] = j['zhanlanshijian']
            item['exh_picture']=exh_picture
            # #
            print("正在爬取展览 " + item['exh_name'] + " ing")
            yield item
        return

    # 主函数
    def parse(self,response):
        exh_id=330500001
        for i in range(1,5):
            exh_id+=100
            exh_url='http://47.98.149.60/hangbo/zhanlan/list?catid=79&&pageNumber=%s'%i+'&&pageSize=6'
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return

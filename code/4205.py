import json

import scrapy
from ..items import *
# import pymysql
'http://www.zhongshanwarship.org.cn/wenwu.html'
'http://www.zhongshanwarship.org.cn/wenwu.html'
class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '4205'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.gthyjng.com/gcww/wwjs/tdgmsq/index.htm']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        body = response.body.decode(response.encoding)
        body = body.replace('jQuery32104839684228954906_1620545767635( ', '')
        body = body.replace(')', '')
        js = json.loads(body)
        i = js['data']
        j = i['dataList']
        for k in j:
            col_name=k['name']
            print(col_name)
        # col_era='null'
        # mus_name='古田会议纪念馆'
        # col_picture='http://www.gthyjng.com/gcww/wwjs/tdgmsq/202004'+response.xpath('//*[@id="fontzoom"]//img/@src').extract()[0].strip('.')
        # col_infod=response.xpath('//*[@id="appendix"]/ul/li/a//text()').extract()
        # col_info="".join(col_infod).strip()
        # col_info=''.join(col_info).replace(' ','')
        # col_info=''.join(col_info).replace('\r','')
        # col_info = ''.join(col_info).replace('\t', '')
        # col_info = ''.join(col_info).replace('\n', '')
        # mus_id=3502
        # item =Item()
        # item['mus_name']=mus_name
        # item['mus_id']=mus_id
        # item['col_id']=response.meta['col_id']
        # item['col_name']=col_name
        # item['col_info']=col_info
        # item['col_picture']=col_picture
        # item['col_era']='null'
        # yield item
        # print("正在爬取藏品 "+item['col_name']+" ing")
        return

    # 藏品列表
    def parse_cols(self, response):
        body=response.body.decode(response.encoding)
        body=body.replace('jQuery32104839684228954906_1620545767635( ','')
        body=body.replace(')','')
        js=json.loads(body)
        i=js['data']
        j=i['dataList']
        for k in j:
            id=k['id']
            new_url='http://pano.bwgyou.com/api/getGoodsById?jsonpCallback=jQuery32107303145991007498_1620550330517&id=%s'%k+'&_=1620550330518'
            yield scrapy.Request(new_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
            response.meta['col_id']+=1

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
        col_id = 350200001
        for i in range(1,4):
            col_id+=100
            col_url='http://pano.bwgyou.com/api/queryGoods?jsonpCallback=jQuery32104839684228954906_1620545767635&page=%s'%i+'&rows=12&museumId=16&tagTemp=1&goodsClassId=24&_=1620545767637'
            yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})

        return
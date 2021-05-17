import json

import scrapy
from ..items import *
# import pymysql

'https://www.shenzhenmuseum.com/api/collection/page/L0302?lang=0&pageNum=1&pageSize=16&platform=0&master='

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '4404'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.bjp.org.cn/kxyj/zpzs/szl/list.shtml']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        url_list = json.loads(response.body)
        print(url_list)
        k=url_list["data"]
        col_name=k["name"]
        print(col_name)
        # mus_name='北京天文馆'
        # col_picture='http://www.bjp.org.cn/'+response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[2]//img/@src').extract()[0]
        # col_info=response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[2]//text()').extract()
        # col_info="".join(col_info).strip()
        # col_info=''.join(col_info).replace(' ','')
        # col_info=''.join(col_info).replace('\r','')
        # col_info = ''.join(col_info).replace('\t', '')
        # col_info = ''.join(col_info).replace('\n', '')
        # col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        # mus_id=1110
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
        url_list=json.loads(response.body)
        tt_url=[]
        i=url_list['data']
        j=i['list']
        for k in j:
            tt_url.append(k['resId'])
        for z in tt_url:
            news_url='https://www.shenzhenmuseum.com/api/collection/get?clazzName=CmsCollection&resId='+z
            yield scrapy.Request(news_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
            response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '北京天文馆'
        item['mus_id'] = 1110
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/p/span/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture='http://www.bjp.org.cn/'+response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div//img/@src')[0].extract()
        item['exh_time'] = "null"
        item['exh_picture']=exh_picture
        # #
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('/html/body/div[3]/div[2]/div[1]/div[2]/div[2]')
        for i in pro:
            news_url=i.xpath('./ul/li/a/@href').extract()
            for j in news_url:
                zl_url='http://www.bjp.org.cn'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1

        return

    # 主函数
    def parse(self,response):
        col_id = 440400001
        for i in range(1,2):
            new_url='https://www.shenzhenmuseum.com/api/collection/page/L0302?lang=0&pageNum=%s'%str(i)+\
                '&pageSize=16&platform=0&master='
            yield scrapy.Request(new_url,callback=self.parse_cols,meta={'col_id':col_id})
            col_id+=100


        # exh_id=111000001
        # exh_id+=100
        # exh_url='http://www.bjp.org.cn/kphd/yzsnt/index.shtml'
        # yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return

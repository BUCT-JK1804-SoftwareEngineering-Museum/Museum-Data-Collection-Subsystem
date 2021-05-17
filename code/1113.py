import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1113'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://nongyebowuguan.meishujia.cn/?act=usite&said=354&usid=394&tag=%E9%99%B6%E7%93%B7']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name='彩陶'
        col_era='null'
        mus_name='中国农业博物馆'
        col_picture1=response.xpath('//table[@style="margin-top: 5px; margin-bottom: 5px;"]//img/@src').extract()
        col_info="null"
        mus_id=1113
        for i in col_picture1:
            col_picture='http://nongyebowuguan.meishujia.cn'+i
            print(col_picture)
            item =Item()
            item['mus_name']=mus_name
            item['mus_id']=mus_id
            item['col_id']=response.meta['col_id']
            item['col_name']=col_name
            item['col_info']=col_info
            item['col_picture']=col_picture
            item['col_era']='null'
            yield item
            response.meta['col_id']+=1
            print("正在爬取藏品 "+item['col_name']+" ing")
        return

    # 藏品列表
    def parse_cols(self, response):
        li=response.xpath('//div[@id="news_content"]/ul')
        for i in li:
            new_url=i.xpath('.//a/@href').extract()
            # print(new_url)
            name=i.xpath('.//a/text()').extract()
            # print(name)

            for j in new_url:
                cp_url='https://www.tjnhm.com/'+j
                yield scrapy.Request(cp_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '中国农业博物馆'
        item['mus_id'] = 1113
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//ul[@class="zl_r_t"]//text()').extract()[1]
        item['exh_name']=exh_name
        exht_info=response.xpath('//ul[@class="zl_r_b zl_r_bt"]//text()').extract()
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
    def parse_exlList(self,response):
        pro=response.xpath('//a[@style="font-size:14px; font-weight:bold;"]/@href').extract()
        for i in pro:
            new_url='http://nongyebowuguan.meishujia.cn'+i
            print('enter:'+new_url)
            yield scrapy.Request(new_url, callback=self.parse_exl, meta={'exh_id': response.meta['exh_id']})
            response.meta['exh_id']+=1

    #主函数
    def parse(self,response):
        col_id = 111300001
        col_id+=1000
        col_url='http://nongyebowuguan.meishujia.cn/?act=usite&said=354&usid=394&tag=%E9%99%B6%E7%93%B7'
        yield scrapy.Request(col_url,callback=self.parse_new,meta={'col_id':col_id})

        exh_id=111300001
        exh_id+=1000
        exh_url='http://nongyebowuguan.meishujia.cn/?act=usite&said=368&usid=394'
        yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id})

        return
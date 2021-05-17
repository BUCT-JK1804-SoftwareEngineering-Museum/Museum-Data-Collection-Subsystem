import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '5108'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.zgshm.cn/imglist.jsp?id=78abd44f3517405da73197aa6e9b0ccb&pageye=1&pageSize=2']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[3]/div/div[1]/div/text()').extract()[0]
        mus_name='自贡市盐业历史博物馆'
        col_picture='http://www.zgshm.cn'+response.xpath('//*[@id="news_conent_two_text"]//img/@src').extract()[0]
        col_infod=response.xpath('//*[@id="news_conent_two_text"]//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=5108
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
        li=response.xpath('/html/body/ul')
        for i in li:
            new_url=i.xpath('./li//a/@href').extract()

            for j in new_url:
                cp_url='http://www.zgshm.cn//'+j
                yield scrapy.Request(cp_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '自贡市盐业历史博物馆'
        item['mus_id'] = 5108
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[3]/div/div[1]/div/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="news_conent_two_text"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        # yy="https://www.tjnhm.com/"
        exh_picture=response.xpath('//*[@id="news_conent_two_text"]//p//img/@src')[0].extract()
        exh_picture='http://www.zgshm.cn'+exh_picture
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('/html/body/ul')
        for i in pro:
            news_url=i.xpath('./li/div/a/@href').extract()
            for j in news_url:
                zl_url='http://www.zgshm.cn/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return
    #主函数
    def parse(self,response):

        exh_id=510800001
        for t in range(1,3):
            exh_id+=100
            exh_url='http://www.zgshm.cn/imglist.jsp?id=78abd44f3517405da73197aa6e9b0ccb&pageye=%s'%str(t)+'&pageSize=2'
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})
        return
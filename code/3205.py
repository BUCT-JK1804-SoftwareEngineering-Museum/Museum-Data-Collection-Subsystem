import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3205'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.hzmuseum.com/#/jibenchenlie']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="aboutus_text"]/h1/text()').extract()[0]
        col_era='null'
        mus_name='天津自然博物馆'
        col_picture='https://www.tjnhm.com/'+response.xpath('////*[@id="aboutus_text"]//img/@src|//*[@id="pagediv"]//img/@src').extract()[0]
        col_infod=response.xpath('//*[@id="aboutus_text"]//p//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        mus_id=1202
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
        # item = Item()
        # item['col_id']=""
        # item['mus_name'] = '杭州博物馆'
        # item['mus_id'] = 3205
        # item['exh_id'] = response.meta['exh_id']
        print('begin')
        exh_name = response.xpath('//*[@id="app"]/div[2]/div/div/text()').extract()[0]
        print(exh_name)
        # item['exh_name']=exh_name
        # exht_info=response.xpath('//div[@id="aboutus_text"]/p//text()').extract()
        # exh_info=''.join(exht_info).strip()
        # exh_info="".join(exh_info).replace(' ','')
        # exh_info=''.join(exh_info).replace('\n','')
        # exh_info=''.join(exh_info).replace('\t','')
        # exh_info=''.join(exh_info).replace('r','')
        # item['exh_info']=exh_info
        # yy="https://www.tjnhm.com/"
        # exh_picture=response.xpath('//*[@id="aboutus_text"]//p//img/@src')[0].extract()
        # if len(exh_picture)<60:
        #     exh_picture=yy+exh_picture
        # item['exh_time'] = 'null'
        # item['exh_picture']=exh_picture
        # print("正在爬取展览 " + item['exh_name'] + " ing")
        # yield item
        return
    #展览列表
    def parse_exlList(self,response):
        for i in range(1,7):
            new_url='http://www.hzmuseum.com/#/consultDetail?id=%s'%str(i)+'&bread=%E5%9F%BA%E6%9C%AC%E9%99%88%E5%88%97&catId=zhanlan'
            yield scrapy.Request(new_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
            print(new_url)
            response.meta['exh_id']+=1
    #主函数
    def parse(self,response):
        # col_id = 120200001
        # for i in range(1,25):
        #     col_id+=1000
        #     col_url='https://www.tjnhm.com/index.php?p=kxyj&lanmu=4&c_id=16&page='+str(i)
        #     yield scrapy.Request(col_url,callback=self.parse_cols,meta={'col_id':col_id})

        exh_id=320500001
        exh_url='http://www.hzmuseum.com/#/jibenchenlie'
        yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id})
        exh_id+=1000
        return
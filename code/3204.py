import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3204'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['https://www.szmuseum.com/Collection/List/ltgb']
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
    def parse_cols1(self, response):
        li=response.xpath('/html/body/div[4]/div[2]/ul')
        print(li)
        for i in li:
            new_url=i.xpath('.//img/@src').extract()
            print(new_url)
        return

    def parse_cols2(self, response):
        li = response.xpath('/html/body/div[4]/div[2]/ul')
        for i in li:
            new_url = i.xpath('.//img/@src').extract()
            print(new_url)
        return

    def parse_cols3(self, response):
        li = response.xpath('/html/body/div[4]/div[2]/ul')
        for i in li:
            new_url = i.xpath('.//img/@src').extract()
            print(new_url)
        return

    def parse_cols4(self, response):
        li = response.xpath('/html/body/div[4]/div[2]/ul')
        for i in li:
            new_url = i.xpath('.//img/@src').extract()
            print(new_url)
        return

    def parse_cols5(self, response):
        li = response.xpath('/html/body/div[4]/div[2]/ul')
        for i in li:
            new_url = i.xpath('.//img/@src').extract()
            print(new_url)
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '天津自然博物馆'
        item['mus_id'] = 1202
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
        pro=response.xpath('//div[@id="news_content"]')
        for i in pro:
            news_url=i.xpath('./div[@class="pro"]/a[1]/@href').extract()
            for j in news_url:
                zl_url='https://www.tjnhm.com/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
    #主函数
    def parse(self,response):
        col_id = 320400001
        new_url1='https://www.szmuseum.com/Collection/List/ltgb'
        yield scrapy.Request(new_url1,callback=self.parse_cols1,meta={'col_id':col_id})
        col_id+=100

        new_url2='https://www.szmuseum.com/Collection/List/mqsh'
        yield scrapy.Request(new_url2, callback=self.parse_cols2, meta={'col_id': col_id})
        col_id += 100

        new_url3='https://www.szmuseum.com/Collection/List/cq'
        yield scrapy.Request(new_url3, callback=self.parse_cols3, meta={'col_id': col_id})
        col_id += 100

        new_url4='https://www.szmuseum.com/Collection/List/gyp'
        yield scrapy.Request(new_url4, callback=self.parse_cols4, meta={'col_id': col_id})
        col_id += 100
        new_url5='https://www.szmuseum.com/Collection/List/zwfch'
        yield scrapy.Request(new_url5, callback=self.parse_cols5, meta={'col_id': col_id})
        col_id += 100
        # exh_id=120200001
        # for t in range(1,5):
        #     exh_id+=1000
        #     exh_url='https://www.tjnhm.com/index.php?p=zlxx&lanmu=2&page='+str(t)
        #     yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return
import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '5002'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['https://www.tjnhm.com/index.php?p=kxyj&lanmu=4&c_id=16&page=1']
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
        li=response.xpath('//div[@class="product-contents "]/a/@href').extract()
        for i in li:
            new_ulr='https://www.hongyan.info/'+i
            yield scrapy.Request(new_ulr, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
            response.meta['col_id'] += 1
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
        pro=response.xpath('/html/body/div[8]/div[2]/div[1]')
        for i in pro:
            news_url=i.xpath('.//div[@class="exhibit-pic"]/a/@href').extract()
            for j in news_url:
                zl_url='https://www.hongyan.info/'+j
                print(zl_url)
                # yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
    #界面列表
    def parse_35(self,response):
        for i in range(1,4):
            new_url='https://www.hongyan.info/index/news_list/c_id/35/m/Home/p/%s'%str(i)+'.html'
            yield scrapy.Request(new_url, callback=self.parse_cols, meta={'col_id': response.meta['col_id']})
    def parse_36(self,response):
        for i in range(1,3):
            new_url='https://www.hongyan.info/index/news_list/c_id/36/m/Home/p/%s'%str(i)+'.html'
            yield scrapy.Request(new_url, callback=self.parse_cols, meta={'col_id': response.meta['col_id']})
    def parse_37(self,response):
        for i in range(1,5):
            new_url='https://www.hongyan.info/index/news_list/c_id/37/m/Home/p/%s'%str(i)+'.html'
            yield scrapy.Request(new_url, callback=self.parse_cols, meta={'col_id': response.meta['col_id']})

    # 主函数
    def parse(self,response):
        col_id = 500200001
        col_url='https://www.hongyan.info/index/news_list/c_id/35/m/Home/p/1.html'
        yield scrapy.Request(col_url,callback=self.parse_35,meta={'col_id':col_id})
        col_id += 1000

        col_url = 'https://www.hongyan.info/index/news_list/c_id/36/m/Home/p/1.html'
        yield scrapy.Request(col_url, callback=self.parse_36, meta={'col_id': col_id})
        col_id += 1000

        col_url = 'https://www.hongyan.info/index/news_list/c_id/37/m/Home/p/1.html'
        yield scrapy.Request(col_url, callback=self.parse_37, meta={'col_id': col_id})
        col_id += 1000

        # exh_id=500200001
        # for t in range(1,6):
        #     exh_id+=100
        #     exh_url='https://www.hongyan.info/index/news_list/c_id/41/m/Home/p/%s'%str(t)+'.html'
        #     yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return
    #
    # 'https://www.hongyan.info/index/news_list/c_id/35/m/Home/p/3.html'
    # 'https://www.hongyan.info/index/news_list/c_id/36/m/Home/p/2.html'
    # 'https://www.hongyan.info/index/news_list/c_id/36/m/Home/p/1.html'
    # 'https://www.hongyan.info/index/news_list/c_id/37/m/Home/p/2.html'
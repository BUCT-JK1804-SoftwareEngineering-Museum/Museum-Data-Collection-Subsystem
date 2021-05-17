import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '6106'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=19']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[4]/div/div[2]/div[1]/h1/text()').extract()[0]
        col_era='null'
        mus_name='古田会议纪念馆'
        col_picture='http://www.gthyjng.com/gcww/wwjs/tdgmsq/202004'+response.xpath('//*[@id="fontzoom"]//img/@src').extract()[0].strip('.')
        col_infod=response.xpath('//*[@id="appendix"]/ul/li/a//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        mus_id=3502
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
        li=response.xpath('//*[@id="brand-waterfall"]')
        for i in li:
            new_url=i.xpath('./div/div/a')
            col_name_all = new_url.xpath('./@title').extract()
            col_picture_all=new_url.xpath('./img/@src').extract()
            for i in range(0,len(col_name_all)):
                col_picture=col_picture_all[i]
                col_name=col_name_all[i]
                col_inf0='null'
                mus_name = '西安半坡博物馆'
                mus_id = 6106
                col_era = 'null'
                col_id=response.meta['col_id']
                response.meta['col_id']+=1
                item = Item()
                item['mus_name'] = mus_name
                item['mus_id'] = mus_id
                item['col_id'] = col_id
                item['col_name'] = col_name
                item['col_info'] = col_inf0
                item['col_picture'] = col_picture
                item['col_era'] = 'null'
                yield item
                print("正在爬取藏品 " + item['col_name'] + " ing")
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '西安半坡博物馆'
        item['mus_id'] = 6106
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//div[@class="shang"]/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//div[@class="ti"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        item['exh_info']=exh_info
        exh_picture='https://bpmuseum.com'+response.xpath('//div[@class="ti"]//img/@src').extract()[0]
        exh_time=response.xpath('//div[@class="xia"]/text()').extract()[0]
        item['exh_time'] = response.xpath('//div[@class="xia"]/text()').extract()[0]
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList1(self,response):
        pro=response.xpath('//*[@id="brand-waterfall"]')
        for i in pro:
            news_url=i.xpath('./div/div/a/@href').extract()
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
        # col_id = 610600001
        # col_id+=100
        # col_url='https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=19'
        # yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})
        # col_id+=100
        # col_url='https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=20'
        # yield scrapy.Request(col_url,callback=self.parse_cols,meta={'col_id':col_id})
        # col_id += 100
        # col_url = 'https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=21'
        # yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})
        # for i in range(1,4):
        #     col_id += 100
        #     col_url = 'https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=20page='+str(i)
        #     yield scrapy.Request(col_url, callback=self.parse_cols, meta={'col_id': col_id})

        exh_id=610600001
        exh_id+=100
        exh_url='https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=39'
        yield scrapy.Request(exh_url, callback=self.parse_exlList1, meta={'exh_id': exh_id, 'url': exh_url})

        return
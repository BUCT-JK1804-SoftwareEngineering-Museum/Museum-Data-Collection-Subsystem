import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1203'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.mzhoudeng.com/relics.aspx?cateid=89']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[1]/div[1]/text()').extract()[0]
        mus_name='周恩来邓颖超纪念馆'
        col_picture='null'
        col_info=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[3]//text()').extract()
        col_info="".join(col_info).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=1203
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
        url_list=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul')
        for li in url_list:
            j=li.xpath('./li/a/@href').extract()
            for i in j:
                new_url='http://www.mzhoudeng.com/'+i
                yield scrapy.Request(new_url, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
                response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '周恩来邓颖超纪念馆'
        item['mus_id'] = 1203
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[1]/div[1]/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[3]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture='null'
        exh_era=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[1]/div[2]/text()').extract()[0]
        item['exh_time'] = exh_era
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul')
        for i in pro:
            news_url=i.xpath('./li/a/@href').extract()
            for j in news_url:
                zl_url='http://www.mzhoudeng.com/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return


    # 主函数
    def parse(self,response):
        # col_id = 120300001
        # for i in range(1,8):
        #     url='http://www.mzhoudeng.com/relics.aspx?cateid=89&page='+str(i)
        #     yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        #     col_id+=100

        exh_id=120300001
        for i in range(1,11):
            exh_id+=100
            exh_url='http://www.mzhoudeng.com/exhibits.aspx?cateid=88&page='+str(i)
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return
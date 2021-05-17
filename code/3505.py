import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3505'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.qzhjg.cn/html/zl/index.html']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[2]/div[2]/ul/div[2]/h1/text()').extract()[0]
        col_era='null'
        mus_name='中国闽台缘博物馆'
        col_picture='http://www.mtybwg.org.cn'+response.xpath('/html/body/div[2]/div[2]/ul/div[1]/div[1]/li/a/img/@src').extract()[0]
        col_infod=response.xpath('/html/body/div[2]/div[2]/ul/div[3]/ul/text()').extract()
        if len(col_infod)==0:
            col_infod.append('null')
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=3505
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
    def parse_dc(self, response):
        li=response.xpath('//*[@id="container"]')
        for i in li:
            new_url=i.xpath('./li/a/@href').extract()
            for j in new_url:
                cp_url='http://www.mtybwg.org.cn/'+j
                yield scrapy.Request(cp_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '中国闽台缘博物馆'
        item['mus_id'] = 3505
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[2]/div[2]/ul/ul[1]/h1/text()').extract()
        if len(exh_name)==0:
            exh_name.append('null')
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[2]/div[2]/ul/ul[2]//text()').extract()
        if len(exht_info)==0:
            exht_info.append('null')
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        yy="http://www.mtybwg.org.cn/"
        exh_picture=response.xpath('/html/body/div[2]/div[2]/ul/ul[2]//img/@src').extract()
        if len(exh_picture)>1:
            exh_picture=yy+exh_picture[1]
        else:
            exh_picture='null'
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        # print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//ul[@class="iflist"]')
        for i in pro:
            news_url=i.xpath('./li//a/@href').extract()
            for j in news_url:
                zl_url='http://www.mtybwg.org.cn/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return
    #主函数
    def parse(self,response):
        # col_id = 350500001
        # for i in range(1,5):
        #     col_url='http://www.mtybwg.org.cn/cangpin/164-%s'%str(i)+'.aspx'
        #     yield scrapy.Request(col_url,callback=self.parse_dc,meta={'col_id':col_id})
        #     col_id+=100
        #
        # col_url='http://www.mtybwg.org.cn/cangpin/113-1.aspx'
        # yield scrapy.Request(col_url, callback=self.parse_dc, meta={'col_id': col_id})
        # col_id += 100
        #
        # col_url = 'http://www.mtybwg.org.cn/cangpin/112-1.aspx'
        # yield scrapy.Request(col_url, callback=self.parse_dc, meta={'col_id': col_id})
        # col_id += 100
        #
        # col_url = 'http://www.mtybwg.org.cn/cangpin/112-2.aspx'
        # yield scrapy.Request(col_url, callback=self.parse_dc, meta={'col_id': col_id})
        # col_id += 100
        #
        # col_url = 'http://www.mtybwg.org.cn/cangpin/110-1.aspx'
        # yield scrapy.Request(col_url, callback=self.parse_dc, meta={'col_id': col_id})
        # col_id += 100



        exh_id=350500001
        for t in range(1,25):
            exh_id+=100
            exh_url='http://www.mtybwg.org.cn/zhanlan2/104-%s'%str(t)+'.aspx'
            yield scrapy.Request(exh_url, callback=self.parse_exlList, meta={'exh_id': exh_id})
        return
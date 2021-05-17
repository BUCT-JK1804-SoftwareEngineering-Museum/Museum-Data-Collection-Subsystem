import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1302'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.xbpjng.cn/wenbotiandi/shuhua.aspx']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lb_Title"]/text()').extract()[0]
        mus_name='西柏坡纪念馆'
        col_picture=response.xpath('//*[@id="main"]/div[3]/div/div[2]/div//img/@src').extract()
        if len(col_picture)<1:
            col_picture="null"
        else:
            col_picture=col_picture[0]
        print(col_picture)
        col_info="null"

        mus_id=1302
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
        url_list=response.xpath('//*[@id="main"]/div[3]/div/div[2]/ul')
        for li in url_list:
            j=li.xpath('./li/a/@href').extract()
            for i in j:
                new_url='http://www.xbpjng.cn/wenbotiandi/'+i
                yield scrapy.Request(new_url, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
                response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '西柏坡纪念馆'
        item['mus_id'] = 1302
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="lb_Title"]/text()|//*[@id="lb_Title"]/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="form1"]/div[3]/div/div[2]/div/div[1]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture="null"
        # if len(exh_picture1)==0:
        #     exh_picture='null'
        # else:
        #     exh_picture=exh_picture1[1]
        exh_era=response.xpath('//*[@id="lb_Time"]/text()').extract()[0]
        item['exh_time'] = exh_era
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="ctl00"]/div[3]/div/div[2]')
        for i in pro:
            news_url=i.xpath('./h2/a/@href').extract()
            for j in news_url:
                zl_url='http://www.xbpjng.cn/News/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return


    # 主函数
    def parse(self,response):
        # col_id = 130200001
        # for i in range(1,5):
        #     url='http://www.xbpjng.cn/wenbotiandi/shuhua.aspx?page='+str(i)
        #     yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        #     col_id+=100
        # for i in range(1, 5):
        #     url = 'http://www.xbpjng.cn/wenbotiandi/wenwu.aspx?page=' + str(i)
        #     yield scrapy.Request(url, callback=self.parse_cols, meta={'col_id': col_id})
        #     col_id += 100
        #
        exh_id=130200001
        for i in range(1,5):
            exh_id+=100
            exh_url='http://www.xbpjng.cn/News/NewsList_New.aspx?id=795&page='+str(i)
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})
        return
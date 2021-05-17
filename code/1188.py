import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '1188'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.printingmuseum.cn/Collection/List/YSSB?pno=YSSB#comehere']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="divBDetail"]/div[2]/h3/text()').extract()[0]
        col_name = "".join(col_name).strip()
        col_name = ''.join(col_name).replace(' ', '')
        col_name = ''.join(col_name).replace('\r', '')
        col_name = ''.join(col_name).replace('\t', '')
        col_name = ''.join(col_name).replace('\n', '')
        col_name = col_name.replace("\u3000", "").replace("\xa0", "")
        mus_name='中国印刷博物馆'
        col_picture=response.xpath('//*[@id="divBDetail"]/div[1]/img/@src').extract()[0]
        col_info="null"
        mus_id=1188
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
        url_list=response.xpath('//*[@id="ulImgList"]')
        for li in url_list:
            new_url_list=li.xpath('./li/a/@href').extract()
            for i in new_url_list:
                new_url='http://www.printingmuseum.cn'+i
                yield scrapy.Request(new_url, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
                response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '中国印刷博物馆'
        item['mus_id'] = 1188
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="htitle"]/text()').extract()[0]
        exh_name = "".join(exh_name).strip()
        exh_name = ''.join(exh_name).replace(' ', '')
        exh_name = ''.join(exh_name).replace('\r', '')
        exh_name = ''.join(exh_name).replace('\t', '')
        exh_name = ''.join(exh_name).replace('\n', '')
        exh_name = exh_name.replace("\u3000", "").replace("\xa0", "")
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="divContent"]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        if(exh_info==''):
            exh_info='null'
        item['exh_info']=exh_info
        exh_picture=response.meta['exh_picture']
        exh_era=response.xpath('//*[@id="spPublicDate"]/text()').extract()[0]
        item['exh_time'] = exh_era
        item['exh_picture']=exh_picture
        #
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="ulBigImgList"]')
        for i in pro:
            news_url=i.xpath('./li/div/div/a/@href').extract()
            picture=i.xpath('./li/img/@src').extract()
            for j in range(0,len(news_url)):
                zl_url='http://www.printingmuseum.cn'+news_url[j]
                exh_picture=picture[j]
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id'],'exh_picture':exh_picture})
                response.meta['exh_id']+=1
        return

    # 主函数
    def parse(self,response):
        # col_id = 118800001
        # for i in range(1,4):
        #     url='http://www.printingmuseum.cn/Collection/List/YSSB?pno=YSSB&page=%s'%i+'&X-Requested-With=XMLHttpRequest'
        #     yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        #     col_id+=100
        # for i in range(1,9):
        #     url='http://www.printingmuseum.cn/Collection/List/YSBC?pno=YSBC&page=%s'%i+'&X-Requested-With=XMLHttpRequest'
        #     yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        #     col_id+=100
        # for i in range(1,5):
        #     url='http://www.printingmuseum.cn/Collection/List/YSJP?subNo=SJ&pno=YSJP&page=%s'%i+'&X-Requested-With=XMLHttpRequest'
        #     yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
        #     col_id+=100


        exh_id=118800001
        for i in range(1,9):
            exh_id+=100
            exh_url='http://www.printingmuseum.cn/Exhibitions/TExhibitionsList/TemporaryExhibition?page=%s'%i+'&X-Requested-With=XMLHttpRequest'
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return

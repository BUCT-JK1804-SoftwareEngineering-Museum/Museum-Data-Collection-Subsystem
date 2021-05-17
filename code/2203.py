import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '2203'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['https://www.wmhg.com.cn/searchs/collection/tpl_file/collection_list/pagesize/9/site_id/0/p/4.html']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('/html/body/div[3]/div/div[1]/div/div/text()').extract()[0]
        col_era='null'
        mus_name='伪满皇宫博物馆'
        col_picture='https://www.wmhg.com.cn'+response.xpath('//div[@class="img"]/img/@src').extract()[0]
        col_infod=response.xpath('//*[@class="p"]//text()').extract()
        col_info="".join(col_infod).strip()
        col_info=''.join(col_info).replace(' ','')
        col_info=''.join(col_info).replace('\r','')
        col_info = ''.join(col_info).replace('\t', '')
        col_info = ''.join(col_info).replace('\n', '')
        col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=2203
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
        li=response.xpath('//*[@id="datalist"]/div[1]')
        for i in li:
            new_url=i.xpath('./div/a/@href').extract()
            for j in new_url:
                cp_url='https://www.wmhg.com.cn'+j
                yield scrapy.Request(cp_url,callback=self.parse_new,meta={'col_id':response.meta['col_id']})
                response.meta['col_id']+=1
        return
    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '伪满皇宫博物馆'
        item['mus_id'] = 2203
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[3]/div/div[1]/div/div/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[3]/div/div[2]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        # yy="https://www.tjnhm.com/"
        exh_picture='https://www.wmhg.com.cn'+response.xpath('/html/body/div[3]/div/div[2]//img/@src')[0].extract()
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return


    #主函数
    def parse(self,response):
        col_id = 220300001
        for i in range(1,5):
            col_id+=100
            col_url='https://www.wmhg.com.cn/searchs/collection/tpl_file/collection_list/pagesize/9/site_id/0/p/%s'%str(i)+'.html'
            yield scrapy.Request(col_url,callback=self.parse_cols,meta={'col_id':col_id})

        exh_id=220300001
        exh_id+=10
        exh_url='https://www.wmhg.com.cn/exhib/detail/55.html'
        yield scrapy.Request(exh_url,callback=self.parse_exl,meta={'exh_id':exh_id})

        exh_id += 10
        exh_url = 'https://www.wmhg.com.cn/exhib/detail/367.html'
        yield scrapy.Request(exh_url, callback=self.parse_exl, meta={'exh_id': exh_id})

        exh_id += 10
        exh_url = 'https://www.wmhg.com.cn/exhib/detail/267.html'
        yield scrapy.Request(exh_url, callback=self.parse_exl, meta={'exh_id': exh_id})

        exh_id += 10
        exh_url = 'https://www.wmhg.com.cn/exhib/detail/1353.html'
        yield scrapy.Request(exh_url, callback=self.parse_exl, meta={'exh_id': exh_id})

        exh_id += 10
        exh_url = 'https://www.wmhg.com.cn/exhib/detail/1890.html'
        yield scrapy.Request(exh_url, callback=self.parse_exl, meta={'exh_id': exh_id})

        exh_id += 10
        exh_url = 'https://www.wmhg.com.cn/exhib/detail/1888.html'
        yield scrapy.Request(exh_url, callback=self.parse_exl, meta={'exh_id': exh_id})

        return
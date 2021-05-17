import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3503'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.qzhjg.cn/html/zl/index.html']
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
        item = Item()
        item['col_id']=""
        item['mus_name'] = '泉州海外交通史博物馆'
        item['mus_id'] = 3503
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div[1]/text()').extract()[0]
        item['exh_name']=exh_name
        exht_info=response.xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        yy="http://www.qzhjg.cn"
        exh_picture=response.xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]//img/@src').extract()
        if len(exh_picture)>1:
            exh_picture=yy+exh_picture[1]
        else:
            exh_picture='null'
        print(response.meta['exh_id'])
        item['exh_time'] = 'null'
        item['exh_picture']=exh_picture
        print("正在爬取展览 " + item['exh_name'] + " ing")
        yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/ul')
        for i in pro:
            news_url=i.xpath('./li/div[@class="thumb"]/a/@href').extract()
            for j in news_url:
                zl_url='http://www.qzhjg.cn/'+j
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1
        return
    #主函数
    def parse(self,response):
        # col_id = 220300001
        # for i in range(1,5):
        #     col_id+=100
        #     col_url='https://www.wmhg.com.cn/searchs/collection/tpl_file/collection_list/pagesize/9/site_id/0/p/%s'%str(i)+'.html'
        #     print(col_url)
        #     # yield scrapy.Request(col_url,callback=self.parse_cols,meta={'col_id':col_id})

        exh_id=350300001
        for t in range(1,11):
            exh_id+=100
            if t!=1:
                exh_url='http://www.qzhjg.cn/html/zl/index_%s'%str(t)+'.html'
            else:
                exh_url='http://www.qzhjg.cn/html/zl/index.html'
            yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        return
import scrapy
from ..items import *
# import pymysql

class FirstSpider(scrapy.Spider):
    #名称,唯一标示
    name = '3202'
    #允许的域名L:限定,平时用不到
    #allowed_domains = ['www.baidu.com']
    #起始的url
    start_urls = ['http://www.19371213.com.cn/collection/featured/']
    # 用于数据解析，相应对象 response

    #单个藏品
    def parse_new(self,response):
        col_name=response.xpath('//*[@id="node-3388"]/section/div[2]/header/h4/text()').extract()[0]
        col_name="".join(col_name).strip()
        col_name=''.join(col_name).replace(' ','')
        col_name=''.join(col_name).replace('\r','')
        col_name = ''.join(col_name).replace('\t', '')
        col_name = ''.join(col_name).replace('\n', '')
        col_name = col_name.replace("\u3000", "").replace("\xa0", "")
        mus_name='侵华日军南京大屠杀遇难同胞纪念馆'
        col_picture='http://www.19371213.com.cn/collection/zdwwjs/202002/'+response.xpath('//div[@class="content-with-social-content"]//img/@src').extract()[0][1:]
        col_info="null"
        # col_info="".join(col_info).strip()
        # col_info=''.join(col_info).replace(' ','')
        # col_info=''.join(col_info).replace('\r','')
        # col_info = ''.join(col_info).replace('\t', '')
        # col_info = ''.join(col_info).replace('\n', '')
        # col_info = col_info.replace("\u3000", "").replace("\xa0", "")
        mus_id=3202
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
        url_list=response.xpath('/html/body')
        for li in url_list:
            j=li.xpath('.//div[@class="card--image"]/a/@href').extract()
            for i in j:
                new_url='http://www.19371213.com.cn/collection/'+i[3:]
                yield scrapy.Request(new_url, callback=self.parse_new, meta={'col_id': response.meta['col_id']})
                response.meta['col_id']+=1
        return

    #单个展览
    def parse_exl(self,response):
        item = Item()
        item['col_id']=""
        item['mus_name'] = '侵华日军南京大屠杀遇难同胞纪念馆'
        item['mus_id'] = 3202
        item['exh_id'] = response.meta['exh_id']
        exh_name = response.xpath('//*[@id="node-3388"]/section/div[2]/header/h4//text()').extract()
        exh_name = ''.join(exh_name).strip()
        exh_name = "".join(exh_name).replace(' ', '')
        exh_name = ''.join(exh_name).replace('\n', '')
        exh_name = ''.join(exh_name).replace('\t', '')
        exh_name = ''.join(exh_name).replace('r', '')
        exh_name = exh_name.replace("\u3000", "").replace("\xa0", "")
        if len(exh_name)<5:
            exh_name="null"
        item['exh_name']=exh_name
        exht_info=response.xpath('//*[@id="node-3388"]/section/div[2]/div//text()').extract()
        exh_info=''.join(exht_info).strip()
        exh_info="".join(exh_info).replace(' ','')
        exh_info=''.join(exh_info).replace('\n','')
        exh_info=''.join(exh_info).replace('\t','')
        exh_info=''.join(exh_info).replace('r','')
        exh_info = exh_info.replace("\u3000", "").replace("\xa0", "")
        item['exh_info']=exh_info
        exh_picture='http://www.19371213.com.cn/exhibition/temporary/202008'+response.xpath('//*[@id="node-3388"]//img/@src')[0].extract()[1:]
        print(exh_picture)
        # item['exh_time'] = "null"
        # item['exh_picture']=exh_picture
        # # #
        # print("正在爬取展览 " + item['exh_name'] + " ing")
        # yield item
        return

    #展览列表
    def parse_exlList(self,response):
        pro=response.xpath('//*[@id="views-bootstrap-grid-1"]/div')
        for i in pro:
            news_url=i.xpath('.//div[@class="card--image"]//a/@href').extract()
            for j in news_url:
                zl_url='http://www.19371213.com.cn/exhibition/temporary'+j[1:]
                yield scrapy.Request(zl_url,callback=self.parse_exl,meta={'exh_id':response.meta['exh_id']})
                response.meta['exh_id']+=1

        return

    # 主函数
    def parse(self,response):
        col_id = 320200001
        for i in range(1,18):
            url='http://www.19371213.com.cn/collection/featured/index_16685_%s'%str(i)+'.html?_=1620483456906'
            yield scrapy.Request(url,callback=self.parse_cols,meta={'col_id':col_id})
            col_id+=100

        exh_id=320200001
        exh_id+=100
        exh_url='http://www.19371213.com.cn/exhibition/temporary/'
        yield scrapy.Request(exh_url,callback=self.parse_exlList,meta={'exh_id':exh_id,'url':exh_url})

        exh_id += 100
        exh_url = 'http://www.19371213.com.cn/exhibition/temporary/index_1.html'
        yield scrapy.Request(exh_url, callback=self.parse_exlList, meta={'exh_id': exh_id, 'url': exh_url})

        return

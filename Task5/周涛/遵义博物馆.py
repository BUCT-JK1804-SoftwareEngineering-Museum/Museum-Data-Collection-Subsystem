
import json
import requests

import random

import os, traceback

from lxml import etree

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    data_title = {}
    data_web={}
    data_contend={}
    number = random.random()
    url='http://www.zunyihy.cn/searchs/collection.html?'+str(number)+'&category_id=&tpl_file=collection&content=&pagesize=9&sort=&p='
    fp = open('./博物馆文物.json', 'w', encoding='utf-8')
    fq = open('./博物馆文物图片.json','w',encoding='utf-8')
    fr = open('./博物馆文物内容.json','w',encoding='utf-8')
    for dit in range(1,6):
        new_url=url+str(dit)
        response = requests.get(url=new_url, headers=headers)
        page_text = response.text
        root = etree.HTML(page_text)
        parpe=root.xpath('//div[@class="img"]//img/@src')
        data=root.xpath('//div[@class="li"]/a[@class="tit"] /@href')
        title=root.xpath('//div[@class="t4 ellipsis"]/text()')
        for ti in title:
            data_title["title"]=ti
            json.dump(data_title, fp, ensure_ascii=False)
        for li in parpe:
            data_web["wb"]='http://www.zunyihy.cn/' + li
            json.dump(data_web, fq, ensure_ascii=False)
        for net in data:
            work_url="http://www.zunyihy.cn/"+net
            work=requests.get(url=work_url,headers=headers)
            print(work)
            work.encoding="utf-8"
            work_dd=work.text
            work_root=etree.HTML(work_dd)
            work_data1=work_root.xpath('//div[@class="situation_1"]//p//text()')
            for wo in work_data1:
                wo=wo.strip()
                if wo!="":
                    data_contend["contend"]=wo
                json.dump(data_contend, fr, ensure_ascii=False)
    fp.close()
    fq.close()
    fr.close()


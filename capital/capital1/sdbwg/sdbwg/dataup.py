# -*- coding = utf-8 -*-
# @Time : 2021/4/29 10:04
# @Author : waynemars
# @File : dataup.py
# @Software : PyCharm
#coding=utf-8
import scrapy
import pymysql
#自定义管道:
class DataConvertPipeLine(object):
    #开启连接:
    def open_spider(self,spider):
        #connect : 充当连接对象.
        self.connect = pymysql.Connect(
            # host、port、user、passwd、db、charset
            host="123.56.13.242",
            port=3306,
            user="root",
            passwd="Aliyun2021",
            db="museum",
            charset="utf8"
        )
        #cur : 充当游标.
        self.cur = self.connect.cursor()
        pass

    #处理item数据,实现存储:
    def process_item(self , item , spider):
        #编写sql实现存储:  item数据的存储.
        # 新增mysql 的语句:  insert into zhilian (字段列表)  values  (' 3000, python工程师 )
        sql = "INSERT INTO Collection(col_id,mus_id,col_name,col_era,col_info,mus_name,col_picture) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(sql,(item["id"],item["mus_id"],item["name"],item["era"],item["introduction"],item["mus_name"],item["image"]))
        #确认提交事务:
        self.connect.commit()
        pass

    #释放资源连接:
    def close_spider(self,spider):
        self.cur.close()
        self.connect.close()
        pass

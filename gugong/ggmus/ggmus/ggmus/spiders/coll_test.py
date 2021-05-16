# import scrapy
# from bs4 import BeautifulSoup
# from pip._vendor import requests
#
# from ..items import GgmusItem
#
# # def next_page():
# #     url = "https://www.dpm.org.cn/explore/collections.html"
# #     # 请求头部
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
# #     # 发送HTTP请求
# #     req = requests.get(url, headers=headers)
# #     # 解析网页
# #     soup = BeautifulSoup(req.text, "lxml")
# #     # 找到name和Description所在的记录
# #     human_list = soup.find({class:'collection1'},{class='box'})("div")
# #
# #     urls = []
# #     # 获取网址
# #     for human in human_list:
# #         url = human.find('a')['href']
# #         urls.append('https://www.wikidata.org' + url)
# #
# #     # print(urls)
# #     return urls
#
# class CollSpider(scrapy.Spider):
#     name = 'coll'
#     allowed_domains = ['https://www.dpm.org.cn/']
#     start_urls = ['https://www.dpm.org.cn/explore/collections.html']
#     base_url = "https://www.dpm.org.cn/"
#
#     i = 0
#     j = 1
#     mus_name_num = '故宫博物院'
#     id_num = 1
#     mus_ida = 1101
#     next_url = []
#
#     #找到目录
#     def parse(self, response):
#         qtqs = response.xpath("//div[@class='collection1']"
#                               "//div[@class='box']/div")
#         for qtq in qtqs:
#             fur = qtq.xpath(".//a/@href").get()
#             # print('#' * 40)
#             # print(self.base_url+fur)
#             # print('#' * 40)
#             # 非数字展品
#             if fur != "/shuziduobaoge.html":# fur = "/collection/ceramics.html"
#                 self.next_url.append(self.base_url+fur)
#         # while self.i < 23:
#         # print('#' * 40)
#         # print(self.next_url[23])
#         # print('#' * 40)
#         #     yield scrapy.Request(self.next_url[self.i], callback=self.next_page, dont_filter=True,
#         #                         meta = {"fur":fur} )
#         yield scrapy.Request(self.next_url[0], callback=self.next_page, dont_filter=True,
#                              meta={"fur": fur})
#
#     def next_page(self,response):
#         fur = response.meta["fur"]
#         page = response.xpath("//div[@class='pages']/a[last()-1]/text()").get()
#         nurl = response.xpath("//div[@class='pages']/a[last()]/@href").get()
#         nurl = nurl[:-6]
#         next = self.base_url + nurl + str(self.j) + ".html"
#         print('#' * 40)
#         print(next)
#         print('#' * 40)
#         # yield scrapy.Request(,callback=self.parse_page, dont_filter=True )
#     def parse_page(self,response):
#         zps = response.xpath("//div[@class='building2']"
#                              "//div[@class='table1']//tr")
#         for zp in zps:
#             name = zp.xpath(".//td[1]/a//text()").getall()
#             name = "".join(name).strip()
#             durl = zp.xpath(".//td[1]/a/@href").get()
#             if durl != None:
#                 durl = durl
#             else: durl=""
#             ima = zp.xpath(".//div[@class='img']/img/@src").get()
#             era = zp.xpath(".//td[2]//text()").getall()
#             era = "".join(era).strip()
#             # print('#' * 40)
#             # print(name)
#             # print(type(self.base_url))
#             # print(type(durl))
#             # print(durl)
#             # print(self.base_url + durl)
#             # print(ima)
#             # print(era)
#             # print('#' * 40)
#             # yield scrapy.Request(self.base_url + durl, callback=self.parse_detail, dont_filter=True,
#             #                      meta = {"name":name, "image":ima} )
#         #
#         # 设置“下一页”
#         next_url = response.xpath("//div[@class='pages']"
#                               "//a[@class='next']/@href").get()
#         if next_url != None:
#             next_url = self.base_url + next_url
#             # 到这个类最后一页，上一级传下来的到达下一个类，i++
#             self.i += 1
#         # a = response.meta["fur"]
#         # a = a[:-10]
#         # # 获得数字编号
#         # b = response.meta["fur"]
#         # b = b[10:]
#         # b = b[1:-11]
#         #
#         # next_url = self.base_url+a+"list_"+b+"_"+str(self.i)+".html"
#         # # 测试网络跳转情况
#         # self.i += 1
#         # # print('#' * 40)
#         # # print(next_url)
#         # # print('#' * 40)
#         # #
#         # c = response.xpath("//ul[@class='pagelist']/li[last()-3]//text()").get()
#         # c = int(c)
#         #
#         # if self.i > c:
#         #     self.i = 2
#         #     return
#         # else:
#         #     yield scrapy.Request(next_url, callback=self.parse_page, dont_filter=True, meta = {"fur":response.meta["fur"]})
#
#     def parse_detail(self, response):
#         name = response.meta["name"]
#         id = str(self.id_num + self.mus_ida * 100000 + 10000)
#         mus_id = str(self.mus_ida)
#         mus_name = self.mus_name_num
#
#         image = response.meta["image"]
#         image = self.base_url + image
#         era = response.xpath("//div[@class='neirong']/ul/li[2]/span[3]//text()").get()
#
#         introduction = response.xpath("//div[@class='neirong']/p//text()").getall()
#         introduction = "".join(introduction).strip()
#         item = GgmusItem(id=id, mus_id=mus_id, name=name, mus_name=mus_name, image=image, era=era,
#                          introduction=introduction)
#         self.id_num += 1
#         yield item
import scrapy

from ..items import QsbkItem

class AhlsmusSpider(scrapy.Spider):
    name = 'ahlsmus'
    allowed_domains = ['http://www.aihuihistorymuseum.org.cn/']
    start_urls = ['http://www.aihuihistorymuseum.org.cn/imglist.aspx?type=377']
    base_domin="http://www.aihuihistorymuseum.org.cn/"
    col_id_num: int = 230310001
    mus_id_num: int = 2303
    col_era_num = '年代：'
    mus_name_num = '瑷珲历史陈列馆'
    def start_requests(self):
        url = "http://www.aihuihistorymuseum.org.cn/imglist.aspx?type=377"
        requests=[]
        for i in range(1,11,1):
            print('#'*40+'1')
            print(i)
            print('#' * 40 + '2')
            data = {
                '__VIEWSTATE':'/wEPDwUKMTA0NzgxMjA4Ng9kFgJmD2QWAgIDD2QWBgICD2QWAgICDxYCHgtfIUl0ZW1Db3VudAIFFgpmD2QWAmYPFQIHaHR0cDovLy8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxNTA1MjYwMTEyNTEyYTllLmpwZ2QCAQ9kFgJmDxUCB2h0dHA6Ly8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNTI2MDExMjQxYTNkYi5qcGdkAgIPZBYCZg8VAgdodHRwOi8vLy9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDE1MDUyNjAxMTIzMmEwYTAuanBnZAIDD2QWAmYPFQIHaHR0cDovLy8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxNTA1MjYwMTEyMjQ0Y2VkLmpwZ2QCBA9kFgJmDxUCB2h0dHA6Ly8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNTI2MDExMjE2MTc5NC5qcGdkAgMPZBYIAgEPDxYCHgRUZXh0BQzppobol4/nsr7lk4FkZAIDDw8WAh8BBQzppobol4/nsr7lk4FkZAIFDxYCHwACEBYgZg9kFgJmDxUDBDIzMDAvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjEwMzE0MDk1ODQ2OWZlZS5qcGcN44CQMjAyMS0wMS4uLmQCAQ9kFgJmDxUDBDIyNTcvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAxMTEzMDE1NTQ1OTc4MC5qcGcN44CQMjAyMC04MC4uLmQCAg9kFgJmDxUDBDIyNTMvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAxMTEyMDk1MjQxMDA3ZS5qcGcN44CQMjAyMC03OS4uLmQCAw9kFgJmDxUDBDIyNDQQaW1hZ2VzL2ltZzAyLmpwZw3jgJAyMDIwLTc4Li4uZAIED2QWAmYPFQMEMjI0MS8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDExMTEwMTMwNDVkMTMzLmpwZw3jgJAyMDIwLTc3Li4uZAIFD2QWAmYPFQMEMjE1NS8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA5MDUwMzI4MjA1NWQxLmpwZw3jgJAyMDIwLTc2Li4uZAIGD2QWAmYPFQMEMjE1Ny8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA5MDUwMzM0MzhlNzIzLmpwZw3jgJAyMDIwLTc1Li4uZAIHD2QWAmYPFQMEMjE1Ni8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA5MDUwMzMwNTdiOGU1LmpwZw3jgJAyMDIwLTc0Li4uZAIID2QWAmYPFQMEMjE0NC8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA4MDgwMTMzNTY1MjY2LmpwZw3jgJAyMDIwLTczLi4uZAIJD2QWAmYPFQMEMjEzOS8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA4MDgwMTE0MTEwZGU0LmpwZw3jgJAyMDIwLTcyLi4uZAIKD2QWAmYPFQMEMjEzMxBpbWFnZXMvaW1nMDIuanBnDeOAkDIwMjAtNzEuLi5kAgsPZBYCZg8VAwQyMTI4Ly9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDgwODEyMjkyMjUxMjYuanBnDeOAkDIwMjAtNzAuLi5kAgwPZBYCZg8VAwQyMTIxLy9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDgwODEyMjkzNTFmZGQuanBnDeOAkDIwMjAtNjkuLi5kAg0PZBYCZg8VAwQyMTA5Ly9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDYyMTEyMTgyN2Q4MmMuanBnDeOAkDIwMjAtNjguLi5kAg4PZBYCZg8VAwQyMTA0Ly9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDYyMTExNTUwNzEyNGEuanBnDeOAkDIwMjAtNjcuLi5kAg8PZBYCZg8VAwQyMDk5EGltYWdlcy9pbWcwMi5qcGcN44CQMjAyMC02Ni4uLmQCBw8PFgQeC1JlY29yZGNvdW50ApIBHhBDdXJyZW50UGFnZUluZGV4AgFkZAIED2QWAmYPFgIfAAIBFgJmD2QWAmYPFQIaaHR0cDovL3d3dy5ob25nYm93YW5nLm5ldC8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNjExMDIyODMyYjNkOS5qcGdkZCIi6cOHAOB17oslsMAX4yx3ZlNpdKq7gXG6uthmuujI',
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$Pager',
                '__EVENTARGUMENT':str(i),
                '__EVENTVALIDATION':'/wEWAwLEsYjMAwLE5MLVAgL9n+DvAfkA5/M9AAqTcRGE85OYX4KQ9Hs1HDsMqImhFxPjI1Ik',
            }

            request = scrapy.FormRequest(url, formdata=data, callback=self.parse)
            # print('#' * 40 + '1')
            # print(request)
            # print('#' * 40 + '2')
            requests.append(request)
        return requests
    def parse(self, response):
        #response = response.document.getElementById()
        print('#' * 40 + '1')
        print(response)
        print('#' * 40 + '2')
        ahdivs = response.xpath("//div[@class='sub_lcon']/div[@class='img_box']")
        for ahdiv in ahdivs:
            col_id = self.col_id_num
            self.col_id_num += 1
            mus_id = self.mus_id_num
            col_era = self.col_era_num
            mus_name = self.mus_name_num
            img_url = ahdiv.xpath(".//a/@href").get()
            print('*'*40+'1')
            print(img_url)
            print('*' * 40 + '2')
            yield scrapy.Request(self.base_domin + str(img_url), callback=self.parse_detail, dont_filter=True,meta={"col_id":col_id,"mus_id":mus_id,"col_era":col_era,"mus_name":mus_name})
        return
    def parse_detail(self,response):
        col_id=response.meta["col_id"]
        mus_id=response.meta["mus_id"]
        col_era=response.meta["col_era"]
        mus_name=response.meta["mus_name"]
        col_name=response.xpath("//div[@class='cgk']/span[@id='ContentPlaceHolder1_title']/text()").get().strip()
        col_picture=response.xpath("//div[@class='sub_artical']//img[1]/@src").get()
        col_picture=self.base_domin+col_picture
        col_info=response.xpath("//div[@class='sub_artical']/span[@id='ContentPlaceHolder1_content']/p//text()").getall()
        col_info="".join(col_info).strip()
        col_info=(str(col_info)).replace("\r","").replace("\n","").replace("\xa0","").replace("\t","")
        item = QsbkItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info, mus_name=mus_name, col_picture=col_picture)
        yield item

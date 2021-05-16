import scrapy

from ..items import QsbkexItem

class AhlsmusSpider(scrapy.Spider):
    name = 'ahlsmusex'
    allowed_domains = ['http://www.aihuihistorymuseum.org.cn/']
    start_urls = ['http://www.aihuihistorymuseum.org.cn/lpiclist.aspx?type=358']
    base_domin="http://www.aihuihistorymuseum.org.cn/"
    exh_id_num: int = 230310001
    mus_id_num: int = 2303
    mus_name_num = '瑷珲历史陈列馆'
    def start_requests(self):
        url = "http://www.aihuihistorymuseum.org.cn/lpiclist.aspx?type=358"
        requests=[]
        for i in range(1,5,1):
            print('#'*40+'1')
            print(i)
            print('#' * 40 + '2')
            data = {
                '__VIEWSTATE':'/wEPDwUKMTA0NzgxMjA4Ng9kFgJmD2QWAgIDD2QWBgICD2QWAgICDxYCHgtfIUl0ZW1Db3VudAIFFgpmD2QWAmYPFQIHaHR0cDovLy8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxNTA1MjYwMTAxMDJlZDQ4LmpwZ2QCAQ9kFgJmDxUCB2h0dHA6Ly8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNTI2MDEwMDUxNjcwYS5qcGdkAgIPZBYCZg8VAgdodHRwOi8vLy9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDE1MDUyNjAxMDAzOGJiMWMuanBnZAIDD2QWAmYPFQIHaHR0cDovLy8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxNTA1MjYwMTAwMTJlNWE2LmpwZ2QCBA9kFgJmDxUCB2h0dHA6Ly8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNTI2MTI1OTU5ZGEwNy5qcGdkAgMPZBYIAgEPDxYCHgRUZXh0BRLkuLTml7blsZXop4jliJfooahkZAIDDw8WAh8BBRLkuLTml7blsZXop4jliJfooahkZAIFDxYCHwACEBYgZg9kFgJmDxUDAzM4NC8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMTAxMTExMTA1NTVkODZhLmpwZxvnkbfnj7Lljoblj7LpmYjliJfppobppoYuLi5kAgEPZBYCZg8VAwMzODMvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAxMTExMDIwOTM5NDlkYy5qcGcZ55O35Lit55S7IOKAlOKAlOeRt+ePsi4uLmQCAg9kFgJmDxUDAzM4MS8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA2MjEwMTU3NDFhMDgyLmpwZxvlsq3kuIrkvKDor7TigJTigJTphILkvKYuLi5kAgMPZBYCZg8VAwMzODIvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAwNjIxMDIyNDExMWI2ZS5qcGcb5Lyg5om/5LiO5Y+R5bGV4oCU4oCU5YyXLi4uZAIED2QWAmYPFQMDMzgwLy9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDYyMTEyNTYxNjIxYTQuanBnG+aWh+WMluWSjOiHqueEtumBl+S6p+aXpS4uLmQCBQ9kFgJmDxUDAzM3OS8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDA2MjExMTUyMDljZGM2LmpwZxvnq6XigJznlLvigJ3lha3kuIDigJTigJQuLi5kAgYPZBYCZg8VAwMzNzgvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAwMjA3MDYxMjE5ZjlhMi5qcGcb5bKt6Ze05pen6ZuG4oCU4oCU6aaG6JePLi4uZAIHD2QWAmYPFQMDMzc3Ly9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDIwMDIwNzA2MDc0NTQ2OTAuanBnG+KAnOWei+KAneaAgeS4h+WNg+KAlOKAlC4uLmQCCA9kFgJmDxUDAzM3Ni8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAyMDAxMzEwODQ1MTcyNGIxLnBuZxvjgIrmtYHlubTkvLzmsLTigJTigJTml6cuLi5kAgkPZBYCZg8VAwMzNzUvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMjAwMTMxMDg0MDEwOGU0Yy5wbmcb5omT6YCg5paH5YyW5Lid57u45LmL6LevLi4uZAIKD2QWAmYPFQMDMzczLy9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDE5MDcyNjAxMzgwMDBiNzguanBnFeWxleiniOWbnumhviB8IOKAnC4uLmQCCw9kFgJmDxUDAzM3MC8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxOTA0MTcxMDQzMjQzYmE2LmpwZxvjgJDlsZXop4jlm57pob7jgJHnkbfnj7IuLi5kAgwPZBYCZg8VAwMzNzEvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTkwNDE3MTIwMDQzZTRmZi5qcGcZ44CQ5bGV6KeI5Zue6aG+44CRIOeRty4uLmQCDQ9kFgJmDxUDAzM3Mi8vbWFuYWdlci9QdWJsaWMvTmV3c2ZpbGUvMjAxOTA0MTcxMjQ0NDZmY2ZhLnBuZxvjgJDlsZXop4jlm57pob7jgJHjgIrlpKcuLi5kAg4PZBYCZg8VAwMzNjkvL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTgwOTI5MDIxOTU5ODQ5NC5wbmcb44CQ5bGV6KeI5Zue6aG+44CR44CK5o6MLi4uZAIPD2QWAmYPFQMDMzY4Ly9tYW5hZ2VyL1B1YmxpYy9OZXdzZmlsZS8yMDE4MDgxNDEwMzQ1ODRkOGYucG5nG+OAkOWxleiniOWbnumhvuOAkeOAiuWNly4uLmQCBw8PFgIeC1JlY29yZGNvdW50AjhkZAIED2QWAmYPFgIfAAIBFgJmD2QWAmYPFQIaaHR0cDovL3d3dy5ob25nYm93YW5nLm5ldC8vL21hbmFnZXIvUHVibGljL05ld3NmaWxlLzIwMTUwNjExMDIyODMyYjNkOS5qcGdkZAf5NSAmKM/q1k+WjjoeCQ5mWlwt40+voIV5fbdR19nn',
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$Pager',
                '__EVENTARGUMENT':str(i),
                '__EVENTVALIDATION':'/wEWAwKXkNuLCQLE5MLVAgL9n+DvASjOXKXfhlHebNrIsXJLc1e2knZyier1uoUWnDFGSMpy',
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
        ahdivs = response.xpath("//div[@class='bd']/ul/li")
        for ahdiv in ahdivs:
            exh_id = self.exh_id_num
            self.exh_id_num += 1
            mus_id = self.mus_id_num
            mus_name = self.mus_name_num
            img_url = ahdiv.xpath(".//a/@href").get()
            print('*'*40+'1')
            print(img_url)
            print('*' * 40 + '2')
            yield scrapy.Request(self.base_domin + str(img_url), callback=self.parse_detail, dont_filter=True,meta={"exh_id":exh_id,"mus_id":mus_id,"mus_name":mus_name})
        return
    def parse_detail(self,response):
        exh_id=response.meta["exh_id"]
        mus_id=response.meta["mus_id"]
        mus_name=response.meta["mus_name"]
        exh_name=response.xpath("//div[@class='jianjie']/span[@class='jj_zi r']/span[@id='ContentPlaceHolder1_content']/p[1]//text()").getall()
        exh_name="".join(exh_name).strip()
        exh_time='临时展厅'
        exh_picture=response.xpath("//div[@class='jianjie']/span[@class='jj_zi r']/span[@id='ContentPlaceHolder1_content']//img[1]/@src").get()
        exh_picture=self.base_domin+str(exh_picture)
        exh_info=response.xpath("//div[@class='jianjie']/span[@class='jj_zi r']/span[@id='ContentPlaceHolder1_content']/p//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_info=(str(exh_info)).replace("\r","").replace("\n","").replace("\xa0","").replace("\t","")
        item = QsbkexItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name,exh_info=exh_info, exh_picture=exh_picture, exh_time=exh_time)
        yield item



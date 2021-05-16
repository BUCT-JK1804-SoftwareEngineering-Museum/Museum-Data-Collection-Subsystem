import scrapy


class WhmusSpider(scrapy.Spider):
    name = 'whmus2'
    #allowed_domains = ['https://www.whmuseum.com.cn']
    start_urls = ['https://www.whmuseum.com.cn']

    def parse(self, response):
        kind=['ceramics','bronze','jade','calligraphy',
              'painting','sculpture','bamboo','col-other']
        page_num=[7,3,4,1,5,1,1,1]
        requests=[]
        for i in range(0,2):#8
            kind_url="https://www.whmuseum.com.cn/collection/"+str(kind[i])
            # print('#' * 40 + '1')
            # print(kind_url)
            # print('#' * 40 + '2')
            url="https://www.whmuseum.com.cn/japi/sw-cms/api/queryExhibitList"
            for j in range(1,int(page_num[i])+1):
                data={
                    # "exhibitLevel":"",
                    # "exhibitName":"",
                    "param":{
                        "pageNum": str(j),
                        "pageSize": '8'
                    }
                }
                print(data)
                yield scrapy.FormRequest(kind_url,formdata=data,callback=self.parse_page,dont_filter=True)
        #         requests.append(response)
        # return requests
        pass
    def parse_page(self,response):
        preview=response.json()
        records=preview['records']
        for record in records:
            col_name=record['exhibitName']
            print('#' * 40 + '1')
            print(col_name)
            print('#' * 40 + '2')
        pass
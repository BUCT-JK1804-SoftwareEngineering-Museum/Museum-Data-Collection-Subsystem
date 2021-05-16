import requests
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }

    products = {}  # 博物馆字典，键值对为藏品名称和详细信息
    url_collect_index = "https://www.hdmuseum.org/Product/Query"
    for PageNum in range(1, 4):
        data = {
            'classId': '16',
            'pageIndex': PageNum,
            'pageSize': '9',
        }
        response = requests.post(url=url_collect_index, data=data, headers=header)
        res = response.json()

        for product in res['list']:
            # 保存到藏品字典
            info = {
                'id': product['id'],
                'productName': product['productName'],
                'description': product['description'],
                'img': "https://www.hdmuseum.org/" + product['img']
            }
            for i in range(2, 6):
                s = "img" + str(i)
                if product[s] != "":
                    info[s] = "https://www.hdmuseum.org/" + product[s]
            # 保存到博物馆字典
            products[product['productName']] = (info)

    with open('hdmuseum.json', 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(products, ensure_ascii=False))

    print("finished!")
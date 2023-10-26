import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

from rakuten_mng.utils.convertext import convert_text


class ScrapingEngine:
    def scrape_item(self, source_url, data, result):
        resp = requests.get(
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        item_detail = dom.find('section', attrs={'class': '__information'})
        data['jan'] = item_detail.find('div', attrs={'class': '__spec'}).table.tr.td.text
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        data['quantity'] = 20 # TODO
        photos = dom.find('div', attrs={'class': '__photo'}).find_all('a')
        for photo in photos:
            url = photo['href']
            data['photos'].append(
                {
                    'url': url
                }
            )
        
        result.append(data)
    
    def scrape_item_list(self, source_url):
        headers = {
            'Cookie': 'b_closed_news=eyJpdiI6InhwZmlJN0hxZ2x2dGNqRk9UL1B4aHc9PSIsInZhbHVlIjoiYWhGWitSL1hUNiswM0xsd0w4L0Q3eWlvRXRFUm92WEJablpFaGRXclArU0xKekdkbU53R05JTlNMajBIN3VWdEFDczdOQnA4MGZtcU1BQjFDQ3pkdGc9PSIsIm1hYyI6IjUwMGEzYWM4YTJlNDIwODUxZjFlMzAwMWRkOTJjNzAzZTRiM2VjNmY2NTAwMmIxYWMyN2Y4NjJkYTdkNmU0YjQifQ%3D%3D; _ga=GA1.1.1938331334.1692600949; _clck=cfyi3l|2|ffy|0|1328; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ild5bnppU0pGS2V3bi9kWmxPaTU2Nmc9PSIsInZhbHVlIjoiUks2VVh5LzkrNmFsc2lSckRzcmhIQlErRnZwSExXS21FWCt2MmM1M2wzWU90U2NialZmb0xtcjlVcmJQOXBQek5rWVI4OWRCQjFRMXVDa0xlTmd3bVdBMGNaQlFRUDBXM0lXMVUyYUdTT1BOVEVXV0ZuQ3FYVHlyVnhHSGNFdVhaNGpNczRyME5hZlVHWVhXa05pcXBLU1NmcmxKbTVkd3JTWVRVWmdZRG1uVHpWRjlaVXF0bUxlMmk2UmVOdXUyaE8zVU5YOHhqcU1CRDhOMlNOZHJZbndvTU9RVUNmaFJxZ25wOU12cFFZWT0iLCJtYWMiOiJlYWRkYTQ2ZmU0NzY2OTA5NWEwNzAzYTdiZWRjM2ZjYWFiYzQ4NmExNzE1N2UwZWU1ZThhM2MwMGIwOGRmNDJkIn0%3D; product_viewed=eyJpdiI6Im9DOW00enhrM3JBY3RXWTFDL0hDWmc9PSIsInZhbHVlIjoiWXAzeFlSNWJDOERYVUt4cmU5aTRLMFRTNC9iM0FOdDRoem1KVWFvMnRzQmZHeEtodW1wbjh3ZFI1UDhpNzhTM3dqWnpPUmxGekM5QnhReE1uS0wxZ0VGdURwN2JLL3pIc2RLY0RNZXJHNURCMm9DdHZCLzNwaDVZcGsvUXRpUm9QdGlqZVJlL0RVSUFjTGpHK0lJeDlBRmdKTDkxbWtDVmp5TWpac1BleHhWcCtqODJFZmRSd2lYM2x4S3VIYnZFdVJYMXRkU2lzY09sM00vRUtlRVdKeDYxd3ZoVE9FVzJuUHIvcGdVOU01QXNIdVNLbW1pV0RQQkJSM09VZmpVRGRoTHA4K29oOVR1ME5DWUZoeTBSUmkreFRDd01GcW44aTdZNzFGM2krZEdsUWx5Tnh6MDc3VmNhKzA5M09VL3JFTnkvRGRTTzNxdzhyZG8xM2NZN0txRkZTd3BzaUN3UjgzVlo2bTNFU0gyQXpMZ0VjTkNreXlLYWI1U2VqK3NkVjBVOCtHbHp3R3lzQWFxOVRSZGl3Wm92Y1RnWDQ2TDhhYXZrZURzZDY5NzlEeVJKc0FxY0NhQVN0WWJSWXlvazhHcEJpbEl2TUlGOVFneXdQT2s1QUhWTmxnSlBVUnNJalkrdDZWU21tQ0xaNUlkZWVWOFZvZDg0RWo5Zm9kM2JTdk9obFNwME1Hbm0xdUY5MG5nZjdnWjRJdFhpalIrOGYxL05yK1Y1dU1FPSIsIm1hYyI6IjgwMDhmNTFhNzhhZDNlYTlmY2U3Yjc4MmNmYzFhNGU4OGEzNTJjMWZhOGZjNDRhN2Q3NWE0OTQ5NDMyZjllNjQifQ%3D%3D; v_style=eyJpdiI6Im5iRUU4YWFPVDFEWE8zdk1JcGNEOUE9PSIsInZhbHVlIjoiM0duLzlSd1VVNFYyTzBWVzZJZ1Z2YUN0Sm5JbU9iR0Iyc0NFYWhFUldGSTczbTJTNk5leTlmTmhKdjNXN29UTyIsIm1hYyI6IjFjMzU3MDM2YzUxMzYyOGMwNjNhZDM3MmVlNzdhYTIyNzI2ZmY0MTA2NWU4MTllOTI2OTEzNzMyN2RjMmY3ODYifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IkVQdFdMOE5TaUprVjdjcXlOOER3YWc9PSIsInZhbHVlIjoiN3hVaUkwQlllSE92Ty82S1gxbVAyRmNUd0Nid2xOdkowZDNQK1NISElkUDFnemZMczVhZ2RoQzRqR2p0ek9BY0svSnV3UEZ4V1pEUEV2QXJ6OGlVUlBFaGtPa3d6bVJ3VWxaY3c3NHFXNmY3enJMVmxPeStMQVFycXFiZzRkajQiLCJtYWMiOiJlNGVjODI1YTFlZGZiOWM2YTFmYmJlNDQ5NjNiZGYxNWI0MDcwZjA1YWM5NmQ0Y2U3Y2FmNmM3MmQzY2Y3NzkxIn0%3D; b_ses=eyJpdiI6Ik1pVWV2V2ViSE93aEVscG1SMW1pZ2c9PSIsInZhbHVlIjoiclRrYXpFVFgxOUJuRWdpY1VPR0I5UnpNNEVKUnFsQkp1bWF5U2JQdG9lOUVwWkkzRjFRdTJNREhSTnRrc2l0UHU2WUx2bUxjeEQ0a3p0UlBrdWxPTnFOVkpEazUvaldVMVJzQlR5NUxYZktmbmZsaU9UekF0Y0huc3d5dkVtUnYiLCJtYWMiOiIyZTBjYTcyN2NlNGVkNjczZDZiYTViM2RlYjJkYmI3NmQ1MmQxZTExYmZlYTA4YjhkZjc1OTYxNDdlM2Q2ZjgwIn0%3D; _ga_KMEM37NKX4=GS1.1.1697628101.39.1.1697628162.59.0.0; _clsk=1m84gyl|1697628163710|7|1|t.clarity.ms/collect'
        }
        response = requests.get(
            headers=headers,
            url=source_url
        )
        dom = bs(response.text, "html.parser")

        result = []
        temp = dom.find('ul', attrs={'class': '__product'}).contents
        items = [item for item in temp if isinstance(item, str) is False and bool(list(filter(lambda x: x=='__is-soldout', item.get('class')))) is False]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)

        for item in items:
            try:
                item_url = item.a['href']
                data = {}
                data['title'] = convert_text(item.find('h2', attrs={'class': '__title'}).text)
                data['source_url'] = item_url
                data['price'] = int(item.find('span', attrs={'class': '__unit-price'}).text.split('円')[0])
                data['count_set'] = int(item.find('span', attrs={'class': '__quantity'}).text)
                data['description'] = data['title']
                data['photos'] = []
                # pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
                self.scrape_item(item_url, data, result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass
        
        pool.shutdown(wait=True)
        return result

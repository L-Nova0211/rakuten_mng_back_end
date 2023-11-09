import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

from rakuten_mng.utils.convertext import convert_text, convert_product_name


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
            'Cookie': 'b_closed_news=eyJpdiI6InhwZmlJN0hxZ2x2dGNqRk9UL1B4aHc9PSIsInZhbHVlIjoiYWhGWitSL1hUNiswM0xsd0w4L0Q3eWlvRXRFUm92WEJablpFaGRXclArU0xKekdkbU53R05JTlNMajBIN3VWdEFDczdOQnA4MGZtcU1BQjFDQ3pkdGc9PSIsIm1hYyI6IjUwMGEzYWM4YTJlNDIwODUxZjFlMzAwMWRkOTJjNzAzZTRiM2VjNmY2NTAwMmIxYWMyN2Y4NjJkYTdkNmU0YjQifQ%3D%3D; product_viewed=eyJpdiI6IjJ0Y3orUXROQVNDY09peFc4anVDaGc9PSIsInZhbHVlIjoiYUpNNURSNDNUdGxJYjAycFU2eEpYdzFHT09XNjhmQjc3SFFBdlI1N3FoODVvWjRWdHQwMHA3RitHTVFDaitpRSt2ajFvbjRzYzBzRFZiTnZmRktpSDdmNjBMS2JnK3Yyck1VclhOc29peVNKWjZvNmhjUElwUGNNcldQQlI1ckM0dDhSMnN4MzZMWEdGZm5XaWZ5WDdQWDFYSW80dGp0OWpDRjlIQ2lML2tmQ0hSZ2RSbjZTbFpZRlJORklzODBRL0NlWGdvNmhuNzl0bkpQODM4MVVXZ1VTVTIrMlQwejk1S0NvbXd6WTdpeWdsYVViM0I2U3R1R2YwL3NSdVJqdWNqRzN0OUl2SjdIaUlrRTNnWU9DMmpMbWh6SlQvd1dPR0Z4SHZOd1JWYlgxcUhSTXVMYnM0M21EdWJmNVJrKzZCajBLTnlKNmt2Zm1JeHFxOHlFc21FamNMSDlBK3IwQTR1Y0hvOVBzZTc3eVVHQmxYUHlhdXFkZmprczZmcmNVRTBNZitrd0RMYkpxTnNPMGJ2Yk9LaUpPVkQra0VoZllXK3lmck94dzdwUzFiR0tnU0xKYXR5M3FVNVNkVXhQaTM0cjZOVk1McFNtVWV6MGdENlFpa2FGVFpFT1pBSmdhVG5vTWZ4UjBleE5ZWTcwYVJHWlBmYzNMbU91N0lvKzBBaGpITldORnI3YitjblVvSytncS9uRldBdlJzMWZyNUhCVzl1eG1oOXRYVEdSdVIyb01JODFiN3BQQXR1Q1MyQmdISEhISXlVWGdiTzduckp4NXJCalladUtSLzM4TTFPUTFuS2VBOU95V01VSXpqWHJSd2R0ZFZLRFlzVUJWK2JQSFBqSldIYU1FcGJPQUg4cXVzZFhTQXZFUFBTanhhOHFXTnYxMjQ1dTg9IiwibWFjIjoiMWU5ZjY1MTk3ODExZWZhNjgzM2Y0ZTE4ZjAyZmI1NWNkYzg5ZjBjMzMyZmRiODcwOWZjNzA0YzA4Y2Q0MDRlYiJ9; _gid=GA1.2.1495066849.1698706891; _clck=cfyi3l|2|fgb|0|1328; v_style=eyJpdiI6IjVqNlozUHFma3A3MEZFQ1pWTFc0bFE9PSIsInZhbHVlIjoiTmdZdVJodHVISTVZK1BLYXA1MHpTZGdLNDhTVno4MzFYemIrdjVnc2FrR3BSZVo4T3FmV2VkQmw4ejQvUlhvMiIsIm1hYyI6IjlkYzIxNTg5NTcyM2U3ZmEwNmEwNzQ1Mzg5YTBkYmY2NTY1YTcxZTdkZThiZjU0NWIxYWRkMDI2YjU2NjFmMzMifQ%3D%3D; XSRF-TOKEN=eyJpdiI6ImNSVmRtajZjK01DaTN0NnVxRk1xN1E9PSIsInZhbHVlIjoiVE9yWFVVSzg1aGlnYUhWUVhpam9JSmQ5VlMzbFhCK0NscXBJVjdZaGZSV3JHa2gvdUNMSFRpSkcrQi95Wk1PMjRSZ1VzVDJ0TEo1MnliVzFRSnl4UFZEWEtLa0lNRi8xcS93QjA1REVKd3dZQ3B1R0VaODcrdlJJdnRjWmlJQ3ciLCJtYWMiOiI0MGRkMzUwZDdkMGNmNDUwYTdlY2U4MDFmNzE4YzQyMzNjOWM2NWE2YTNlYjM1N2EzNjEwMTY4NDgwZTQ3M2UyIn0%3D; b_ses=eyJpdiI6IjY4Q1J4dWpvUmw5THlxMWJtdUZCSGc9PSIsInZhbHVlIjoidkxmU25CNkdqWWdYbm9HMTVtWnYzaThhZWluZXo1Szd0NlJpL2FUcUlCcmtzVGtJYm11ZGsrWkxLNE5kYUNNbGp5b0haU0hNNVBmeHdZRUtUMWRWSnY3eFByTmVRd0c1VzdSM1hnUW5ETEFjdTBpaFBPM3lPTFdFcmtMNHNtMzAiLCJtYWMiOiJiNGY0MzU1NGQ4NjQ3NWZiNTNkZjE3MjRjY2MxZjc5MWEwNThhMTIxYWVhOTQzNGIxYWM4ZDljMDE2M2FkMmY3In0%3D; _ga_KMEM37NKX4=GS1.1.1698766410.50.1.1698771334.27.0.0; _ga=GA1.2.1938331334.1692600949; _gat_gtag_UA_36869509_1=1; _clsk=j1ylzh|1698771336439|18|1|t.clarity.ms/collect'
        }
        response = requests.get(
            headers=headers,
            url=source_url
        )
        from_product_index = response.text.find('<section class="__list __list--row">')
        temp = response.text[from_product_index:]
        to_product_index = temp.find('</section>')
        dom = bs(temp[:to_product_index], 'html.parser')

        result = []
        temp = dom.find('ul', attrs={'class': '__product'}).contents
        items = [item for item in temp if isinstance(item, str) is False and bool(list(filter(lambda x: x=='__is-soldout', item.get('class')))) is False]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)

        for item in items:
            try:
                item_url = item.a['href']
                data = {}
                data['title'] = convert_text(item.find('h2', attrs={'class': '__title'}).text)
                data['title'] = convert_product_name(data['title'])
                data['source_url'] = item_url
                data['price'] = int(item.find('span', attrs={'class': '__unit-price'}).text.split('円')[0])
                data['count_set'] = int(item.find('span', attrs={'class': '__quantity'}).text)
                data['title'] = f'{data["title"]} {data["count_set"]}個セット'
                data['description'] = data['title']
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass
        
        pool.shutdown(wait=True)
        return result

import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

from rakuten_mng.utils.convertext import convert_text, convert_product_name


class ScrapingEngine:
    def __init__(self) -> None:
        self.headers = {
            'Cookie': 'v_style=eyJpdiI6IjVqNlozUHFma3A3MEZFQ1pWTFc0bFE9PSIsInZhbHVlIjoiTmdZdVJodHVISTVZK1BLYXA1MHpTZGdLNDhTVno4MzFYemIrdjVnc2FrR3BSZVo4T3FmV2VkQmw4ejQvUlhvMiIsIm1hYyI6IjlkYzIxNTg5NTcyM2U3ZmEwNmEwNzQ1Mzg5YTBkYmY2NTY1YTcxZTdkZThiZjU0NWIxYWRkMDI2YjU2NjFmMzMifQ%3D%3D; _ga=GA1.1.1938331334.1692600949; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ik15SjFDd1gyYTkybjdxVUh6Z1UwdWc9PSIsInZhbHVlIjoiU3dhekRvK3REam1oZkZ6Nm9hM0tMRkFoSkJLMEQxenBFcFRmRnliV2cxUjJObEFaWGNMOWtsalNUWVlZZ3A4cEVaZTJMbWd1dG9VQjNrZG11MmVmbzl2Qzl5SEcwSjNwckY0Q3lUclc2anRjUWpVb1NaQVlXbU13WjRVbG1nSDJQeUJvc0hXUUZiVUk3ODQzS3EvQlpINHlKQnhYcytNUXFYWHZJaGtIK2V1SmRWdTlPQXlsZ1E1Z1hVWlFMSko3c1pLbExpeGZ5S09CaVZTWGNia3B3SmRIVEg0akpCSjJjeHhrMnVCTmxZMD0iLCJtYWMiOiIwODMzYjNkNTFlMjc4OTAyOTBjODA2YTdmNjZiY2UxYzAzYzRiM2FiNWY1NTU4NzkxNjA4MDJiY2Y4YmZlZDNiIn0%3D; _clck=cfyi3l%7C2%7Cfgs%7C0%7C1328; product_viewed=eyJpdiI6InhYK1JTbmhEN3YzR0d3bGFsNjJ1UFE9PSIsInZhbHVlIjoiWUFJODhuQXkwdE43Z3lsTmtHcVlkU2JpeUQ4SngrNVl1K2ZrekE4OXNxeEpydW93dWM0WUF2MDFqeGtnK2Qwek5JZTJWYlU1eGV6dWFjVFdpcmd4V1RhY3hiMXZQeVhLaHBkSVo4SVRQbnh5NE1hSENKNk9IQm5pMzNVblptZnhoUm44dndVeGo3T0Q0NWpZbUZCb3A0cE1UNklTdkM3T3VIS3lzamU3dENHS2VPVzJjNEkzWjN4YjkrNUQ5Q1BFQ1I1ampXemFSaUJYOXBOMmI2OWtKOXZhYlJGdm44N0kvUE9ERW9nMHk2bDRhOXcybkVoMUZheUgyOVN5TWkybkdFRmFYUWVKOVNxSzVsdkw3VVpYNEdXdDA0U3prQVVPUElTaDRmRHN3eGE4RDhBalNTR0dURGhlY2NncjUxM2lLbTYvQUFoeXdRaHhDZkszYUs5eG4zNjhteUdibk1JRmt3cDRvTUhJcmcydmZmMlpnWkphY2RNK2hnSG5iOENKMXZtSURVV0tUekduMnEzOUpqNGhsdXovNjJnWWw1UXFXTGovT1YvYW52NlpzaWxNclBad3h6eXFjYno1SitJNUNleHdWWUwxb2J5cjRZamNGZ2thejdkb010dFJEZ1BPZUtKMjF4VTFNWW1FYWdwK09YNmhQeFA0K2owTkt0RTRGQU1kT2pIaldLUVpFVG9RampOZEJJZXh4Z0I4NjVacUYyVjFmcTBJT0VPSWtYbGtVRHBRL0hHRENMR3U0a1h6SDJRSGdpK2VIU1N4d2dqSVVCalVkeFhIODNCSGM3ZkhFSHdSaEdoZVhSSEFKVXRWTkFpUG11ZnBJN0RoWGlhMFVxcTduZUZhSUR4RS85RE15S1g3VStBZ0FJdlYyKzcweFRFTk1PUW04WFJia2NmYVB5VDRXeXFUd0xnSFVSZ3EiLCJtYWMiOiJjMDIxY2ZhYWQ1MGEyZjYyYWMzMGM5MGZjNjFlMzRmMmYzYzRhNjY3ZDNkYzZjZTkyOGJjNjgxNmU4ZjVmMjEyIn0%3D; _ga_KMEM37NKX4=GS1.1.1700179368.61.0.1700179368.60.0.0; _clsk=myrq2q%7C1700179369135%7C2%7C1%7Ct.clarity.ms%2Fcollect; b_closed_news=eyJpdiI6ImJGSEhNZ1pSbTlRb3VYN25xWmpwdnc9PSIsInZhbHVlIjoiZ3k5amE2WUQ5QkZxdDhIWEtsY2lVRHEvQjJjc3FKckxaam9nMG9Zd3dBYlBlaGRlR1Rvc1FMZUVXSVU0QmZZNXhHc2FEQWswbkVISzFhZUpDYnB1Tlg2dlpES1NPUzkrV0RsbUJ1WjloNFk9IiwibWFjIjoiYTEzNmMxN2YxOTY1YjFiNzQxMGJmMGY0NDg0M2I1ZjFjOTliZGRmODNlMDc2ZDA5N2IyYzdjZWVhMzE4NDYyZiJ9; XSRF-TOKEN=eyJpdiI6IkFCY290VDJIT2x3TndKRmFpZllkZ1E9PSIsInZhbHVlIjoiNDhBb1BIRDJMYjYyQStuL0JmNGFtdGQzUHczazkrMFAwL0dSdThEZ1FvM2owU2Q0eVU4ZFhsZDlPSUtKUjE1emVGTVJxb2VZNWg5L2Nla21VaGgyUmFMUU8wWXh1V1NKTTVPUy9YaHhDVnNCRTB4Zm5NeHIvclE2VEhrS1hKRloiLCJtYWMiOiI4NTlhODgwNzI4NGZkZTljZmRjNTRlN2U4ODdiZTIwNmJiMmEwM2IxMzgxMTFlYzAyMjVhYWJhZWYwZGQzNzY4In0%3D; b_ses=eyJpdiI6IkhpUzgydTBGS3hxMlFOUmx4NHM5RFE9PSIsInZhbHVlIjoiQVlLNG14L3N5ZTdmZDdNbW0xdVJlb3VMNmxiSkF3amdkZWZGeUcxSW9RS3gydFZaaTZPdUc4L3V1RmFkUWJKSDUrVU9UUERocVo4Mjd5VUI2Ukl6M3IyV0J0Y1lZSlVCcUtLSTIxZm8yUVd2OU82YUhFTTNoNWJHV2tEWUhXOVciLCJtYWMiOiIwMWZmYjllZjM3ZTJjZGI4M2UzNzIyODQ4NmU0ZDYwZGY5M2VlZjVhNGJkZDI2YzM1NTYyN2JlZjFkODgyZGNkIn0%3D'
        }

    def scrape_item(self, source_url, data, result):
        resp = requests.get(
            headers=self.headers,
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        item_detail = dom.find('section', attrs={'class': '__information'})
        data['jan'] = item_detail.find('div', attrs={'class': '__spec'}).table.tr.td.text
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        data['price'] = int(float(dom.find('span', attrs={'class': '__unit-price'}).text.split('円')[0].replace(',', '')))
        data['count_set'] = int(dom.find('span', attrs={'class': '__quantity'}).text)
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
        response = requests.get(
            headers=self.headers,
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
                data['description'] = data['title']
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass
        
        pool.shutdown(wait=True)
        for item in result:
            item['title'] = f'{item["title"]} {item["count_set"]}個セット'            
        return result

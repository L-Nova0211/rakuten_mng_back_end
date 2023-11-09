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
            'Cookie': 'v_style=eyJpdiI6IjVqNlozUHFma3A3MEZFQ1pWTFc0bFE9PSIsInZhbHVlIjoiTmdZdVJodHVISTVZK1BLYXA1MHpTZGdLNDhTVno4MzFYemIrdjVnc2FrR3BSZVo4T3FmV2VkQmw4ejQvUlhvMiIsIm1hYyI6IjlkYzIxNTg5NTcyM2U3ZmEwNmEwNzQ1Mzg5YTBkYmY2NTY1YTcxZTdkZThiZjU0NWIxYWRkMDI2YjU2NjFmMzMifQ%3D%3D; product_viewed=eyJpdiI6IldyY2JWRFk4bE56dUlEVFh5Z2J1V3c9PSIsInZhbHVlIjoiU3gvbHA0bWhvbXdmNjBVRG5xK21ITm81MW43d3BGcHJ5N2lYS0VCWVBmb0NPWnVKTFNHcnFZUjI0MmpGOS9CTjNodVFldU1QMWFPRnZjQ2hpVGRVNjA2WHgyVVhuUnJrWGRkMUxjL1ZqdFU5SVBEdWROQXRrU1JmZER2aHR4Vk50ODRlTllYRVlleXpoam4xb21pRGRzck56UWc5ajVCMDdhNHpob05FZEN4RHhjVDd4YkdpemdTaFYzNWFzaTdNb2dCa2YxakVqME9qRnh2YmlocGM0VjZ3YVk5c3J2dWllTjd0MWdnbStlM2NYNEFQUDJlSkZac3RhcmVHY2VzaWhNN09XTndybm1Jd0YreFdGY0hoZVVOQ0Q4cllsYUcycFIvVS9VNHJXTVJTYUdXaDQ4bXRVLzI0RWlCSDVqaVpXMXhzT0ZIRnU1T3hTek05TWpmVDhYc0poREpXMzJoTXhOOVhML080TGZBMWdRa1ZVanVBQjU3cVlrNUdwNmZkUU5JZXhlcXBvVnBaUGNEZ0NwWnIxdlJEOENxMGFzV095eERJaWZ2VXBSVGJYd21wSnpsT09wMnhZRHU1WTJ4ZE82M3U4MENaM1hBYk8xdTFEVS9kRzgrcmw0M1BwMlVBZHVGWHpNTUlhd2FONVY1dm9CazFLVGp4UUU0Y1k2UEY3UFNuMXZ5VkMxVVgwbTlEMDh5Y2FyZWE0cUJLSFh6Ulo2WERJNU5VeWVLa0w3YkJmcGdmT2FCSWM4eWRaMHJiT0pranE5aHRzQldlZG80NVRHQ2hzcFJ6Z0M3RG5LMitqZlJGT0JzcHBYQUZ4eFhJQnJlVFJqd3BoNjlCSnY5WVFkMkpjV1B6YVVsc1VQd0xQd3BXUW4rc0YycENFcXVQVU9Ta1RKVTZvd2hQRXpDQ20vOTdzM0QrVFpYemRoMlQiLCJtYWMiOiJhMjBjZmI3M2ZmZWFlMzQ4NWMyMTcwYzBiNDk4NGIzMjc4MjU5Mzg3MGQ5OWZhYmMwZTEzNDljNjc5MGIwNTBjIn0%3D; _ga=GA1.1.1938331334.1692600949; b_closed_news=eyJpdiI6InBGVGxISGFqWTRCT0JEa3d5ay9KK0E9PSIsInZhbHVlIjoiM1k4NXJmb3BWQnY5T3NhSlE5dktlUFdJMitGZG9LRUxaY1lueXFwQytiVXgrSTJrYWhSSEJuSVU5SzlSaWQ1U3E1NDZqc3JRck9wN0tQMy8rOWRiZEhETTVmOS9CT012eGRkUGJJR0FlVkU9IiwibWFjIjoiNTU1ZGUzZjFhZDk5MGE2YmI2MWZkMTAxZTkwODFjZWYxOWY0M2NkZDUzN2ZkMWZmZTBlNjZhMmRhODU1YWJmNSJ9; _clck=cfyi3l|2|fgk|0|1328; XSRF-TOKEN=eyJpdiI6ImE3NkhhTTFaUTE4bTZDeUxvSGRHelE9PSIsInZhbHVlIjoidHh4d25zM3NuaGE4SThtUzFJZ1JwVFp5MEdQdGt2RHliczhLUUxBdEl5a1JLNzRFWUY0bHJUZVBXV054cDFHdFZmYUpKZ2dHNkJNaG50YXdsdHdEUTN5QWgybklyOFEyNXFaZWRiQlFsWVNMcytkT0luSmZhbkxhZjNucmFhd00iLCJtYWMiOiI2NjZlMDYzOTdjZTU1N2Y4N2JjMDU1MDBhZjVhMDQ3NTQ0MjYwNmNiMTVkZWJiYzJkNzdlZDE3MGU4N2IyZjcyIn0%3D; b_ses=eyJpdiI6Ii90aVZRZktSTFlqVC9vbDdKdDNzbnc9PSIsInZhbHVlIjoiVStWbzFMQ1NyYWtjUlRRZDBybllkUnNJV3BxblJ5RWljd2NWOE9xR1lpNXRVUTBDc3FnSDh4Z1crejJlbUgvYndtUFBhYUhrU1pwRUc5QXltdXZ0Z0dHcnpzck9SdDVnTlEyZW15ZGpBZE1MdkpNRGxuWE9USzB1WHgrNC9XdmIiLCJtYWMiOiI3MjM1ZGI5MWFjNTY0OTZlM2Q1NzhmMmE0OGI1YmFjNTkyNzc4Yzk5MDkzNTZlMGUzNjhhNTc3ZmY1NmY1ZTA3In0%3D; _ga_KMEM37NKX4=GS1.1.1699532793.57.1.1699533133.59.0.0; _clsk=1nj99rb|1699533135083|4|1|q.clarity.ms/collect'
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

import concurrent.futures
import re
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
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        pattern = r'\d+'
        data['price'] = int(re.findall(pattern, convert_text(item_detail.find('div', attrs={'class': '__spec'}).table.find_all('tr')[-1].text))[0])
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
        resp = requests.get(
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        result = []
        temp = dom.find('ul', attrs={'class': '__product'}).contents
        items = [item for item in temp if isinstance(item, str) is False]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)

        for item in items:
            try:
                item_url = item.a['href']
                data = {}
                data['title'] = convert_text(item.find('h2', attrs={'class': '__title'}).text)
                data['source_url'] = item_url
                data['description'] = data['title']
                data['photos'] = []
                # pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
                self.scrape_item(item_url, data, result)
            except Exception:
                raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                # pass
        
        pool.shutdown(wait=True)
        return result

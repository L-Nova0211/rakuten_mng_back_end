import concurrent.futures
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from rakuten_mng.utils.convertext import convert_text


class ScrapingEngine:
    def scrape_item(self, source_url, data, result, driver):
        resp = requests.get(
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        # item_detail = dom.find('div', attrs={'id': 'dp-container'})
        # data['description'] = []
        # descriptions = item_detail.find('div', attrs={'id': 'feature-bullets'}).ul.find_all('span', attrs={'class': 'a-list-item'})
        # for description in descriptions:
        #     data['description'].append(convert_text(description.text))
        
        pattern = r'"large":"https://m.media-amazon.com.*?.jpg'
        matches = re.findall(pattern, dom.find('div', attrs={'id': 'imageBlock_feature_div'}).find_all('script')[2].text)
        for item in matches:
            url = item.split('"')[-1]
            data['photos'].append(
                {
                    'url': url
                }
            )
        
        result.append(data)
    
    def scrape_item_list(self, source_url):
        options = webdriver.ChromeOptions() 
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(source_url)
        dom = bs(driver.page_source, "html.parser")
        result = []
        items = dom.find_all('div', attrs={'class', 'a-section a-spacing-base'})
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(items))

        for item in items:
            try:
                item_url = f"https://www.amazon.co.jp{item.contents[-1].find('div', attrs={'class': 'a-section a-spacing-none a-spacing-top-small s-title-instructions-style'}).h2.a['href']}"
                data = {}
                data['title'] = convert_text(item.contents[-1].find('div', attrs={'class': 'a-section a-spacing-none a-spacing-top-small s-title-instructions-style'}).h2.text)
                data['source_url'] = urllib.parse.unquote(item_url)
                if item.contents[-1].find('span', attrs={'class': 'a-price'}):
                    price_dom = item.contents[-1].find('span', attrs={'class': 'a-price'}).find('span', attrs={'class': 'a-offscreen'})
                else:
                    price_dom = item.contents[-1].find('span', attrs={'class': 'a-color-price'})
                data['price'] = int(price_dom.text.split('￥')[-1].replace(',', ''))
                data['description'] = data['title']
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result, driver=driver)
            except Exception:
                # raise ValueError(item.contents[-1].find('div', attrs={'class': 'a-section a-spacing-none a-spacing-top-small s-title-instructions-style'}).h2.text)
                pass

        pool.shutdown(wait=True)
        return result

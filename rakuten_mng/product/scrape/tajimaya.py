import time
import concurrent.futures
import re
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from rakuten_mng.utils.convertext import convert_text


class ScrapingEngine:
    def scrape_item(self, source_url, data, result):
        resp = requests.get(
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        item_detail = dom.find('section', attrs={'class': '__information'})
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        photos = item_detail.find('div', attrs={'class': '__photo'}).find('div', attrs={'class': '__main'}).find_all('a')
        for photo in photos:
            url = photo['href']
            data['photos'].append(
                {
                    'url': url
                }
            )
        
        result.append(data)
    
    def scrape_item_list(self, source_url):
        login_url = 'https://www.tajimaya-oroshi.net/login.php'
        options = webdriver.ChromeOptions() 
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(login_url)
        actions = ActionChains(driver)

        # Login
        input_email = driver.find_element(By.NAME, "loginEmail")
        assert input_email.is_enabled()
        actions.move_to_element(input_email).click().send_keys('tsuneyasu.4100@gmail.com').perform()

        input_password = driver.find_element(By.NAME, "loginPassword")
        assert input_password.is_enabled()
        actions.move_to_element(input_password).click().send_keys('RTest1234').perform()

        input_remember = driver.find_element(By.NAME, "remember")
        assert input_remember.is_enabled()
        actions.move_to_element(input_remember).click().perform()

        btn_login = driver.find_element(By.NAME, "login")
        assert btn_login.is_enabled()
        actions.move_to_element(btn_login).click().perform()

        # driver.execute_script("window.open('');")
        # # Switch to the new window and open new URL
        # driver.switch_to.window(driver.window_handles[1])
        driver.get(source_url)
        dom = bs(driver.page_source, "html.parser")

        # Get Products
        result = []
        temp = dom.find('ul', attrs={'class': '__product'}).contents
        items = [item for item in temp if isinstance(item, str) is False]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(items))

        for item in items:
            try:
                item_url = item.a['href']
                data = {}
                data['title'] = convert_text(item.find('h2', attrs={'class': '__title'}).text)
                data['source_url'] = item_url
                data['description'] = data['title']
                data['price'] = int(float(item.find('span', attrs={'class': '__unit-price'}).text.split('円')[0]))
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass

        pool.shutdown(wait=True)
        return result
    
from importlib import import_module

from rakuten_mng.utils.scrape_site import scraping_site


def select_engine(url):
    result = ''
    for key, value in scraping_site.items():
        if key in url:
            result = value
            break

    if result:
        module = import_module(f'product.scrape.{result}')
        engine = getattr(module, 'ScrapingEngine')
        return engine
    
    return 

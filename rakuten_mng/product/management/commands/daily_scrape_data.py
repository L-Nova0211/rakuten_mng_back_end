import concurrent.futures
import schedule
import time
from django.core.management.base import BaseCommand

from rakuten_mng.product.models import Product
from rakuten_mng.product.scrape.engineselector import select_engine
from rakuten_mng.utils.profit_util import calc_profit
from rakuten_mng.utils.rms_api import InventoryAPI


class Command(BaseCommand):
    def daily_scrape_data(self):
        products = Product.objects.all()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=30)
        result = []
        for product in products:
            url = product.source_url
            engine = select_engine(url=url)
            if engine:
                engine = engine()
                try:
                    data = {}
                    data['photos'] = []
                    data['pk'] = product.id
                    pool.submit(engine.scrape_item, source_url=url, data=data, result=result)
                except Exception as err:
                    print(err)
                
        pool.shutdown(wait=True)
    
        for item in result:
            try:
                product = Product.objects.get(pk=item['pk'])
                if item.get('quantity'):
                    profit = calc_profit(
                        sell_price=product.sell_price,
                        buy_price=item['price'],
                        count_set=item['count_set'],
                        shipping_fee=product.shipping_fee,
                        point=product.point
                    )
                    product.buy_price = item['price']
                    product.count_set = item['count_set']
                    product.profit = profit
                else:
                    product.quantity = 0
                    inventory_data = {
                        "mode": "ABSOLUTE",
                        "quantity": 0
                    }
                    inventory_api = InventoryAPI(service_secret=product.created_by.service_secret, license_key=product.created_by.license_key)
                    inventory_api.register_inventory_stock(
                        manage_number=product.manage_number,
                        variant_id=product.manage_number,
                        data = inventory_data
                    )
                product.save()
            except Exception as err: 
                print(err)

    def handle(self, *args, **options):
        schedule.every().day.at('07:00').do(self.daily_scrape_data)
        while True:
            schedule.run_pending()
            time.sleep(1)
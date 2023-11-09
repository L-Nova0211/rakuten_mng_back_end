import csv
import datetime
import schedule
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from rakuten_mng.product.models import Product, ProductSetting
from rakuten_mng.utils.rms_api import OrderAPI
from rakuten_mng.utils.elastic_mail_api import ELASTICEMAILAPI


class Command(BaseCommand):
    def send_daily_order(self):
        products = Product.objects.filter(status='Active')
        product_setting = ProductSetting.objects.get(created_by=products[0].created_by)
        service_secret = product_setting.service_secret
        license_key = product_setting.license_key
        order_api = OrderAPI(service_secret, license_key)

        now = datetime.datetime.now()
        start_date = now-datetime.timedelta(1)
        # Generate Search Order Data
        search_data = {
            'dateType': 1,
            'startDatetime': f'{start_date.year}-{start_date.month}-{start_date.day}T08:00:00+0900',
            'endDatetime': f'{now.year}-{now.month}-{now.day}T08:00:00+0900',
            "PaginationRequestModel" : {
                "requestRecordsAmount" : 1000,
                "requestPage" : 1,
                "SortModelList" : [
                    {
                        "sortColumn" : 1,
                        "sortDirection" : 1
                    }
                ]
            }
        }
        resp = order_api.search_orders(search_data)
        if resp.status_code < 300:
            order_num_list = resp.json()['orderNumberList']
            # Get Order List
            order_data = {
                'orderNumberList': order_num_list,
                'version': '7'
            }
            resp = order_api.get_order(order_data)
            if resp.status_code < 300:
                # Generate CSV File
                order_list = resp.json()['OrderModelList']
                if order_list:
                    with open(file=str(settings.APPS_DIR / f'media/{now.year}-{now.month}-{now.day}.csv'), mode='w', encoding='utf-8-sig', newline='') as f:
                        field_names = ['注文日', '注文ID', '商品番号', '商品名', '商品ID', '商セット数', '注文件数', '合計数']
                        writer = csv.DictWriter(f, fieldnames=field_names)
                        writer.writeheader()

                        for order in order_list:
                            item_model_list = order['PackageModelList'][0]['ItemModelList']
                            for item in item_model_list:
                                # Write Order Info
                                count_set = item['itemNumber'].split('-')[-1]
                                writer.writerow({
                                    '注文日': order['orderDatetime'], 
                                    '注文ID': order['orderNumber'],
                                    '商品番号': item['itemNumber'],
                                    '商品名': item['itemName'], 
                                    '商品ID': item['itemId'], 
                                    '商セット数': count_set, 
                                    '注文件数': item['units'], 
                                    '合計数': item['units']*int(count_set)
                                })

        if order_list:
            email_api_key = settings.EMAIL_API_KEY
            email_api = ELASTICEMAILAPI(email_api_key)
            email_data = {
                'from': settings.BACKEND_EMAIL,
                'to': products[0].created_by,
                'subject': 'Daily Report',
                'bodyHtml': 'This is daily report.'
            }
            with open(file=str(settings.APPS_DIR / f'media/{now.year}-{now.month}-{now.day}.csv'), mode='rb') as f:
                file_content = f.read()
            attachment = [(
                f'{now.year}-{now.month}-{now.day}.csv',
                file_content
            )]
            email_api.send_email(data=email_data, attach=attachment)
        

    def handle(self, *args, **options):
        schedule.every().day.at('08:00').do(self.send_daily_order)
        while True:
            schedule.run_pending()
            time.sleep(1)

import base64
import requests


class CabinetAPI:
    def __init__(self, service_secret, license_key) -> None:
        self.main_url = 'https://api.rms.rakuten.co.jp/es/1.0/cabinet'
        self.auth_key = base64.b64encode(f'{service_secret}:{license_key}'.encode()).decode()
        self.headers = {
            'Authorization': f'ESA {self.auth_key}'
        }

    def insert_image(self, data):
        url = f'{self.main_url}/file/insert'
        self.headers['Content-Type'] = 'multipart/form-data'
        resp = requests.post(
            headers=self.headers,
            url=url,
            data=data,
            files=data
        )
        return resp


class ItemAPI:
    def __init__(self) -> None:
        pass

    def insert_item(self):
        pass


class InventoryAPI:
    def __init__(self) -> None:
        pass

    def register_inventory_stock(self):
        pass

import base64
import requests


class CabinetAPI:
    def __init__(self, service_secret, license_key) -> None:
        self.main_url = 'https://api.rms.rakuten.co.jp/es/1.0/cabinet'
        self.auth_key = base64.b64encode(f'{service_secret}:{license_key}'.encode()).decode()
        self.headers = {
            'Authorization': f'ESA {self.auth_key}'
        }

    def search_files(self, file_path):
        url = f'{self.main_url}/files/search?filePath={file_path}'
        resp = requests.get(
            headers=self.headers,
            url=url
        )
        return resp
    
    def get_files_in_folder(self, folder_id):
        url = f'{self.main_url}/folder/files/get?folderId={folder_id}'
        resp = requests.get(
            headers=self.headers,
            url=url
        )
        return resp
    
    def insert_folder(self, data):
        url = f'{self.main_url}/folder/insert'
        resp = requests.post(
            headers=self.headers,
            url=url,
            data=data
        )
        return resp
    
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

    def remove_image(self, data):
        url = f'{self.main_url}/file/delete'
        resp = requests.post(
            headers=self.headers,
            url=url,
            data=data
        )
        return resp


class ItemAPI:
    def __init__(self, service_secret, license_key) -> None:
        self.main_url = 'https://api.rms.rakuten.co.jp/es/2.0/items'
        self.auth_key = base64.b64encode(f'{service_secret}:{license_key}'.encode()).decode()
        self.headers = {
            'Authorization': f'ESA {self.auth_key}'
        }

    def insert_item(self, manage_number, data):
        url = f'{self.main_url}/manage-numbers/{manage_number}'
        resp = requests.put(
            headers=self.headers,
            url=url,
            json=data
        )
        return resp

    def patch_item(self, manage_number, data):
        url = f'{self.main_url}/manage-numbers/{manage_number}'
        resp = requests.patch(
            headers=self.headers,
            url=url,
            json=data
        )
        return resp


class InventoryAPI:
    def __init__(self, service_secret, license_key) -> None:
        self.main_url = 'https://api.rms.rakuten.co.jp/es/2.0/inventories'
        self.auth_key = base64.b64encode(f'{service_secret}:{license_key}'.encode()).decode()
        self.headers = {
            'Authorization': f'ESA {self.auth_key}'
        }

    def register_inventory_stock(self, manage_number, variant_id, data):
        url = f'{self.main_url}/manage-numbers/{manage_number}/variants/{variant_id}'
        resp = requests.put(
            headers=self.headers,
            url=url,
            json=data
        )
        return resp

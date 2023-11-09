import requests


class ELASTICEMAILAPI:
    def __init__(self, api_key) -> None:
        self.main_url = 'https://api.elasticemail.com/v2'
        self.api_key = api_key

    def send_email(self, data, attach=None):
        url = f'{self.main_url}/email/send'
        data['apiKey'] = self.api_key
        resp = requests.post(
            url=url,
            params=data,
            files=attach
        )
        return resp

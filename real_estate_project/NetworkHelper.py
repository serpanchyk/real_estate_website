import requests

class NetworkHelper:
    def __init__(self, api_url, token=None):
        self.api_url = api_url
        self.token = token
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

    def get_list_api(self):
        items = requests.get(f"{self.api_url}/", headers=self.headers)
        return items.json()

    def get_item_api(self, item_id):
        return requests.get(f"{self.api_url}/{item_id}/", headers=self.headers).json()

    def create_item_api(self, data):
        return requests.post(f"{self.api_url}/", json=data, headers=self.headers).json()

    def update_item_api(self, item_id, data):
        return requests.put(f"{self.api_url}/{item_id}/", json=data, headers=self.headers).json()

    def delete_item_api(self, item_id):
        return requests.delete(f"{self.api_url}/{item_id}/", headers=self.headers)


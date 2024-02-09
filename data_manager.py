import os
from dotenv import load_dotenv
import requests

load_dotenv('.env')


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_endpoint = 'https://api.sheety.co/52d0e86a43ac5f22aa892f89acbb9d94/flightDeals/prices'
        self.user_endpoint = 'https://api.sheety.co/52d0e86a43ac5f22aa892f89acbb9d94/flightDeals/users'
        self.headers = {'Authorization': os.getenv('SHEETY_TOKEN')}

    def get_sheet_data(self):
        response = requests.get(url=self.sheet_endpoint, headers=self.headers)
        return response.json()["prices"]

    def update_iata_code(self, object_id, city_data):
        body = {'price': city_data}
        response = requests.put(url=f'{self.sheet_endpoint}/{object_id}', json=body, headers=self.headers)
        print(response.text)

    def get_user_data(self):
        response = requests.get(url=self.user_endpoint, headers=self.headers)
        return response.json()

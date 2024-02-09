import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv('.env')
flight_location_endpoint = 'https://api.tequila.kiwi.com/locations/query'
flight_search_endpoint = 'https://api.tequila.kiwi.com/v2/search'


class FlightSearch:
    def __init__(self):
        self.headers = {'apikey': os.getenv('FLIGHT_SEARCH_APIKEY')}

    def get_iata_code(self, city):
        query = {'term': city, }
        response = requests.get(url=flight_location_endpoint, params=query, headers=self.headers)
        return response.json()

    def search_flight(self, departure_city, destination):
        date_from = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        to_date = (datetime.now() + (timedelta(days=30) * 6)).strftime('%d/%m/%Y')

        query = {
            'fly_from': departure_city,
            'fly_to': destination,
            'date_from': date_from,
            'date_to': to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            'curr': 'GBP',
        }

        response = requests.get(url=flight_search_endpoint, params=query, headers=self.headers)
        response.raise_for_status()

        try:
            data = response.json()['data'][0]
        except IndexError:
            query['max_stopovers'] = 2
            response = requests.get(url=flight_search_endpoint, params=query, headers=self.headers)
            data = response.json()['data'][0]

            flight_data = FlightData(
                departure_city=data['route'][0]['cityFrom'],
                departure_airport=data['route'][0]['cityCodeFrom'],
                destination_city=data['route'][1]['cityTo'],
                destination_airport=data['route'][1]['cityCodeTo'],
                price=data['price'],
                fly_from=data['route'][0]['local_departure'],
                fly_to=data['route'][-1]['local_departure'],
                stop_overs=1,
                via_city=data['route'][0]['cityTo'],
            )
        else:
            flight_data = FlightData(
                departure_city=data['route'][0]['cityFrom'],
                departure_airport=data['route'][0]['cityCodeFrom'],
                destination_city=data['route'][0]['cityTo'],
                destination_airport=data['route'][0]['cityCodeTo'],
                price=data['price'],
                fly_from=data['route'][0]['local_departure'],
                fly_to=data['route'][-1]['local_departure'],
                stop_overs=0,
                via_city=None,
            )
        finally:
            return flight_data

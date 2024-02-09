import json
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


DEPARTURE_CITY = 'LON'

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# with open('sheet_data.json', 'w') as f:
#     json.dump(data_manager.get_sheet_data(), f, indent=4)

with open('sheet_data', 'r') as f:
    sheet_data = json.load(f)

low_price_alert = ''

for city in sheet_data:
    # if iata code is not in the sheet get iata code for tequila location api and update sheet data
    if not city['iataCode']:
        city['iataCode'] = flight_search.get_iata_code(city['city'])['locations'][0]['code']
        data_manager.update_iata_code(object_id=city['id'], city_data=city)

    flight_data = flight_search.search_flight(departure_city=DEPARTURE_CITY, destination=city['iataCode'])
    # if not flight data skip to next iteration
    if not flight_data:
        continue
    # If price from result is lower than price in the sheet, create the message
    elif flight_data.price < city['lowestPrice']:
        message = (f'\nLow price alert! Only £{flight_data.price} to fly from {flight_data.departure_city}'
                   f'-{flight_data.departure_airport} to {flight_data.destination_city}-'
                   f'{flight_data.destination_airport}, form {flight_data.fly_from[:10]} to '
                   f'{flight_data.return_date[:10]}.\n')
        # if there are stop-overs add this to message
        if flight_data.stop_overs > 0:
            message += f'Flight has {flight_data.stop_overs} stop over, via {flight_data.via_city} city.\n'
        low_price_alert += message

# with open('user_data.json', 'w') as f:
#     json.dump(data_manager.get_user_data(), f, indent=4)

with open('user_data.json', 'r') as f:
    user_data = json.load(f)['users']
# send email
for user in user_data:
    notification_manager.send_email(
        name=f"{user['firstName']} {user['lastName']}",
        email=user['email'],
        message=low_price_alert,
    )
# Send the message
# notification_manager.send_message(low_price_alert)


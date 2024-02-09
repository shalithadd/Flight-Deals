class FlightData:
    def __init__(self, departure_city, departure_airport, destination_city, destination_airport, price,
                 fly_from, fly_to, stop_overs, via_city):
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.price = price
        self.fly_from = fly_from
        self.return_date = fly_to
        self.stop_overs = stop_overs
        self.via_city = via_city

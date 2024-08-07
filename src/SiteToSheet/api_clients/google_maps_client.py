import googlemaps

from datetime import datetime
from datetime import timedelta

class GoogleMapsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
        self.transport_mode = "transit"
        self.start = None
        self.next_monday = None
        self.nearby_stations = None

    def set_start(self, start, transport_mode = "transit"):
        """Sets start location and transport mode"""
        self.transport_mode = transport_mode
        self.start = start
        self.next_monday = (datetime.today() + timedelta(days=-datetime.today().weekday(), weeks=1)).replace(hour=9, minute=0, second=0, microsecond=0)  

    def time_to_destination(self, destination, start = None ):
        """Returns time to destination"""
        if start is None :
            start = self.start
 
        dist = self.gmaps.distance_matrix(
            start,
            destination,
            mode=self.transport_mode,
            arrival_time = self.next_monday
            )
        duration=dist["rows"][0]["elements"][0]["duration"]["text"]
        return duration

    def nearest_station(self):
        """
        Finds the nearest station to the starting location.

        This function uses the Google Maps API to geocode the
        starting address and then finds the nearest station within
        a 600 meter radius. The function returns a tuple containing the
        name of the nearest station and its location.

        Returns:
            tuple: A tuple containing the name of the nearest station and its location.
        """
        geo_loc = self.gmaps.geocode(address=self.start)
        geo_lat_long = geo_loc[0]['geometry']['location']
        nearest_station = self.gmaps.places_nearby(
            location=geo_lat_long,
            radius=600,
            keyword="tube station"
            )
        stations_list=nearest_station['results']
        stat_list=[]
        try:
            tube_list=open('../utils/tube_stops.txt', encoding="UTF-8").read().splitlines()
        except NotADirectoryError as e:
            print(f"Could not find tube list at ../utils/tube_stops.txt, {e}")
        for i in stations_list:
            if any(word in i['name'] for word in tube_list):
                stat_list.append((i['name'],i['geometry']['location']))

        self.nearby_stations = stat_list
        return stat_list[0]
    
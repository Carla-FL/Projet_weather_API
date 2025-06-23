import httpx
from src.models.input_models import (
    OpenWeatherGeocoding, 
    OpenWeatherAPIResponse
)

def get_coord_from_city(c):
    # appeler api geocoding
    # source: https://openweathermap.org/api/geocoding-api
    # requete api 
    d = None
    d = OpenWeatherGeocoding(d)
    return 

def get_weather_from_city(c):
    # step 1 : call geocoding
    # step 2 : call openweatherapi with lon, lat
    return 
import httpx
from src.models.input_models import (
    OpenWeatherGeocoding, 
    OpenWeatherAPIResponseModel
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
    fields = get_coord_from_city(c)
    lon = fields.lon
    lat = fields.lat
    # step 2 : call openweatherapi with lon, lat
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={TOKEN}"
    res = httpx.get(URL).json()

    if res.status_code == 200:
        return OpenWeatherAPIResponseModel(
                temp = res.get('temp'),
                feels_like = res.get('feels_like'),
                pressure = res.get('pressure'),
                humidity = res.get('humidity'),
                dew_point = res.get('dew_point'),
                uvi = res.get('uvi'),
                clouds = res.get('clouds'),
                visibility = res.get('visibility'),
                wind_speed = res.get('wind_speed'),
                wind_deg = res.get('wind_deg')
                )
    return None
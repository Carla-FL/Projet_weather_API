import httpx, os
from src.models.input_models import (
    OpenWeatherGeocoding, 
    OpenWeatherAPIResponse
)

TOKEN = os.getenv("api_key_open_weather", "")

def get_coord_from_city(city_name: str="", country_code: str="", state_code: str="", limit=1) -> OpenWeatherGeocoding:
    """
    appeler api geocoding - source: https://openweathermap.org/api/geocoding-api
    """

    location = f"{city_name}"
    if state_code: location += f",{state_code}"
    if country_code: location += f",{country_code}"
    URL = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={TOKEN}"
    
    res = httpx.get(URL, timeout=10)
    if res.status_code == 200:
        d = OpenWeatherGeocoding()
    return 

def get_weather_from_city(c):
    # step 1 : call geocoding
    # step 2 : call openweatherapi with lon, lat
    return 
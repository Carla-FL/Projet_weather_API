import httpx, os, dotenv
from functools import lru_cache
from src.models.input_models import (
    OpenWeatherGeocodingModel, 
    OpenWeatherAPIResponseModel
)
from src.models.response_models import SingleSourceModelRep

dotenv.load_dotenv()
TOKEN = os.getenv("api_key_open_weather", "")

@lru_cache(2048)
def get_coord_from_city(city_name: str="", country_code: str="", state_code: str="", limit=1) -> OpenWeatherGeocodingModel:
    """
    appeler api geocoding - source: https://openweathermap.org/api/geocoding-api
    """

    location = f"{city_name}"
    if state_code: location += f",{state_code}"
    if country_code: location += f",{country_code}"
    URL = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={TOKEN}"
    
    res = httpx.get(URL, ) # timeout=30)
    if res.status_code == 200:
        d = res.json()[0]
        return OpenWeatherGeocodingModel(
            name=d.get('name'),
            lat=d.get('lat'),
            lon=d.get('lon'),
            country=d.get('country'),
            state=d.get('state')
        )
    else:
        return None

def get_weather_from_openweather(c):

    # step 1 : call geocoding
    fields = get_coord_from_city(c)

    if not fields:
        return None
    
    lon = fields.lon
    lat = fields.lat

    # step 2 : call openweatherapi with lon, lat
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={TOKEN}"
    res = httpx.get(URL)
    return SingleSourceModelRep(source="openweather")
    
    # if res.status_code == 200:
    #     res = res.json()
    #     return OpenWeatherAPIResponseModel(
    #         temp = res.get('temp'),
    #         feels_like = res.get('feels_like'),
    #         pressure = res.get('pressure'),
    #         humidity = res.get('humidity'),
    #         dew_point = res.get('dew_point'),
    #         uvi = res.get('uvi'),
    #         clouds = res.get('clouds'),
    #         visibility = res.get('visibility'),
    #         wind_speed = res.get('wind_speed'),
    #         wind_deg = res.get('wind_deg')
    #         )
    # return None
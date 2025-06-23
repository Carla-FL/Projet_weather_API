import httpx
from src. controllers.openweather import get_coord_from_city
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

om = openmeteo_requests.Client()

def get_weather_from_openmeteo(c):
    fields = get_coord_from_city(c)
    lon = fields.lon
    lat = fields.lat
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={TOKEN}"
    res = httpx.get(URL)

    if res.status_code == 200:
        res = res.json()
        params = {
            "latitude": lat,
            "longitude": lon
            }

        responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        return responses
    return None
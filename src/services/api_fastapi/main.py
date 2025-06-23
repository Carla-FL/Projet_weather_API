import dotenv, os, fastapi
from src.controllers import openmeteo, openweather, weatherapi

dotenv.load_dotenv()
app = fastapi.FastAPI()

@app.get("/")
def start():
    return {"reponse": "welcome"}


@app.get("/meteo/<city_name>")
def load_meteo_from_city(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openweather.get_weather_from_city(city_name)
    return {}

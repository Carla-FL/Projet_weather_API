import dotenv, os, fastapi, sys, uvicorn
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.controllers import openmeteo, openweather, weatherapi
from fastapi.exceptions import HTTPException

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
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res

@app.get("/meteo/openmeteo/<city_name>")
def load_meteo_from_openmeteo(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openmeteo.get_weather_from_openmeteo(city_name)
    print(res)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res

if __name__ == '__main__':
    uvicorn.run("src.services.api_fastapi.main:app", host="127.0.0.1", port=8025, reload=True)

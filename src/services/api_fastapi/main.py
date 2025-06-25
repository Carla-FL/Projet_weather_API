import dotenv, os, fastapi, sys, uvicorn
from fastapi.exceptions import HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.controllers import openmeteo, openweather, weatherapi, merge


dotenv.load_dotenv()
app = fastapi.FastAPI()

@app.get("/")
def start():
    return {"reponse": "welcome"}


@app.get("/meteo/openweather/<city_name>")
def load_meteo_from_city_with_openweather(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openweather.get_weather_from_city(city_name)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res


@app.get("/meteo/openmeteo/<city_name>")
def load_meteo_from_city_with_openmeteo(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openmeteo.get_weather_from_openmeteo(city_name)
    print(res)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res


@app.get("/meteo/multisource/<city_name>")
def load_meteo_mutisource(city_name: str=""):
    if not city_name:
        raise HTTPException(status_code=400, detail="city name is required")
    try:
        return merge.get_multisource_meteo(city_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in get_multisource_meteo : {str(e)}")

if __name__ == '__main__':
    uvicorn.run("src.services.api_fastapi.main:app", host="127.0.0.1", port=8025, reload=True)

import dotenv, os, fastapi, sys, uvicorn
from fastapi.exceptions import HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.controllers import openmeteo, openweather, weatherapi, merge


dotenv.load_dotenv()
app = fastapi.FastAPI()

@app.get("/health")
def health_check():
    return {"reponse": "ok"}


@app.get("/meteo/current/openweather/")
def load_meteo_from_city_with_openweather(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openweather.get_weather_from_city(city_name)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res


@app.get("/meteo/current/openmeteo/")
def load_meteo_from_city_with_openmeteo(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = openmeteo.get_weather_from_openmeteo(city_name)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res


@app.get("/meteo/current/weatherapi/")
def load_meteo_from_city_with_weatherapi(city_name: str=None):
    if not city_name:
        return {"error": "city name required !"} # ajouter status code erreur
    res = weatherapi.get_weather_from_weatherapi(city_name)
    if res is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return res


@app.get("/meteo/current/")
def load_meteo_mutisource(city_name: str=""):
    if not city_name:
        raise HTTPException(status_code=400, detail="city name is required")
    try:
        return merge.get_multisource_meteo(city_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in get_multisource_meteo : {str(e)}")


@app.get("/meteo/forecast/")
def load_forecast_from_city(city_name: str=""):
    if not city_name:
        raise HTTPException(status_code=400, detail="city name is required")
    try:
        return {} # merge.get_forecast(city_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in get_forecast : {str(e)}")


@app.get("/meteo/history/")
def load_history_from_city(city_name: str="", days: int=7):
    if not city_name:
        raise HTTPException(status_code=400, detail="city name is required")
    try:
        return {} # merge.get_history(city_name, days)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in get_history : {str(e)}")


if __name__ == '__main__':

    FASTAPI_HOST = os.getenv("fastapi_host", "")
    FASTAPI_PORT = int(os.getenv("fastapi_port", 8000))
    
    if (not FASTAPI_HOST) or (not FASTAPI_PORT):
        raise ValueError("FASTAPI environment variables are not set correctly. Please set fastapi_host and fastapi_port in your .env file.")
    
    uvicorn.run(
        "src.services.api_fastapi.main:app", 
        host=FASTAPI_HOST, port=FASTAPI_PORT, reload=True
        )

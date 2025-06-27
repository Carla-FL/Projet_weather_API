import httpx, os, dotenv
from src.controllers.openmeteo import get_coord_from_city
from src.models.response_models import (
    SingleSourceModelRep,
    Localisation, InformationsTemporelles, 
    Temperature, ConditionsMeteorologiques, Vent
)    

dotenv.load_dotenv()
TOKEN = os.getenv("api_key_weather_api", "")


def get_weather_from_weatherapi(cityname) -> SingleSourceModelRep: 

    # etape 1 : récup les longitude et latitude en partant du nom de la ville
    fields = get_coord_from_city(cityname)
    lon = fields.lon
    lat = fields.lat

    # etape 2
    url = f"https://api.weatherapi.com/v1/current.json?q={cityname}&key={TOKEN}"
    res = httpx.get(url)

    if res.status_code == 200:
        res = res.json()
        print(res.keys())
        return SingleSourceModelRep(
            source = "weatherapi",
            localisation=Localisation(
                longitude=str(res["location"]["lon"]),
                latitude=str(res["location"]["lat"]),
                pays=str(res["location"]["country"]),
                ville=str(res["location"]["name"]),
            ),
            informations_temporelles=InformationsTemporelles(
                current_time=str(res["location"]["localtime"]),
            ),
            temperature=Temperature(
                actuelle=str(res["current"]["temp_c"]),
                ressentie=str(res["current"]["feelslike_c"]),
                min=str(res["current"]["temp_c"]),
                max=str(res["current"]["temp_c"]),
                unité="°C"
            ),
            conditions_meteorologiques=ConditionsMeteorologiques(
                etat="",
                description="",
                humidité=str(res["current"]["humidity"]),
                pression=str(res["current"]["pressure_mb"]) + " mb",
                visibilité=str(res["current"]["vis_km"]) + " km"
            ),
            vent=Vent(
                vitesse=str(res["current"]["wind_kph"]),
                direction="",
                unité="km/h"
            )
        )
    else:
        # types erreurs 
        # cf swagger https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2#/
        print({"error": "No data found for the specified city.", "source": "weatherapi"})
        return SingleSourceModelRep(source="weatherapi")
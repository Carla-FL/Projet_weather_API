import openmeteo_requests
import numpy as np
from openmeteo_sdk.Variable import Variable
from openmeteo_sdk.Aggregation import Aggregation
from src.controllers.openweather import get_coord_from_city
from src.models.response_models import SingleSourceModelRep, Localisation, InformationsTemporelles, Temperature, ConditionsMeteorologiques, Vent

# dotenv.load_dotenv()
# TOKEN = os.getenv("api_key_open_weather", "")
om = openmeteo_requests.Client()

def get_weather_from_openmeteo(c) -> dict:
        """
        Faire un appel api vers la source openmeteo.
        """

        # etape 1 : récup les longitude et latitude en partant du nom de la ville
        fields = get_coord_from_city(c)
        lon = fields.lon
        lat = fields.lat
        ville = fields.name
        pays = fields.state # ou fields.contry

        # etape 2 : appel api en passant par le client
        params = {
        "latitude": lat,
        "longitude": lon,
        "temperature_unit": "celsius",
        "wind_speed_unit" : "kmh",
        "forecast_days": 1,
        "current": ["apparent_temperature", "temperature_2m", "wind_speed_10m", "wind_direction_10m","relative_humidity_2m", "pressure_msl", "visibility"],
        "daily" :["temperature_2m_max","temperature_2m_min"]
        }
        res = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        if res is None:
                return None
        else:
                response = res[0]
                print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
                print(f"Elevation {response.Elevation()} m asl")
                print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
                print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

                current = response.Current()
                current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
                current_apparent_temperature = next(filter(lambda x: x.Variable() == Variable.apparent_temperature, current_variables))
                current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
                current_wind_speed_10m = next(filter(lambda x: x.Variable() == Variable.wind_speed and x.Altitude() == 10, current_variables))
                current_wind_direction_10m = next(filter(lambda x: x.Variable() == Variable.wind_direction and x.Altitude() == 10, current_variables))
                current_relative_humidity_2m = next(filter(lambda x: x.Variable() == Variable.relative_humidity and x.Altitude() == 2, current_variables))
                current_pressure = next(filter(lambda x: x.Variable() == Variable.pressure_msl , current_variables))
                current_visibility = next(filter(lambda x: x.Variable() == Variable.visibility, current_variables))

                

                daily = response.Daily()
                daily_variables = list(map(lambda i: daily.Variables(i), range(0, daily.VariablesLength())))
                temperature_2m_max = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2 and x.Aggregation() == Aggregation.maximum, daily_variables))
                temperature_2m_min = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2 and x.Aggregation() == Aggregation.minimum, daily_variables))



                """
                Créations de variables 
                """
                Vent(
                        vitesse=str(current_wind_speed_10m.Value()),
                        direction=str(current_wind_direction_10m.Value()),
                        unité="km/h"
                )

                Temperature(
                        actuelle=str(current_temperature_2m.Value()),
                        ressentie=str(current_apparent_temperature.Value()),
                        min=str(temperature_2m_min.ValuesAsNumpy()[0]),
                        max=str(temperature_2m_max.ValuesAsNumpy()[0]),
                        unité="°C"
                )

                ConditionsMeteorologiques(
                        etat="",
                        description="",
                        humidité=str(current_relative_humidity_2m.Value()),
                        pression=str(current_pressure.Value()),
                        visibilité=str(current_visibility.Value())
                )
                Localisation(
                        longitude=str(response.Longitude()),
                        latitude=str(response.Latitude()),
                        pays=str(pays),
                        ville=str(ville)
                )
                InformationsTemporelles(
                        current_time=str(response.Current().Time())
                )

                return "ok"

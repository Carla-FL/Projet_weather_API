import openmeteo_requests
from openmeteo_sdk.Variable import Variable
from src. controllers.openweather import get_coord_from_city

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
        "current": ["apparent_temperature", "temperature_2m"],
        "daily" :["temperature_2m_max","temperature_2m_min"]
        }
        res = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        if res is None:
                return None
        else:
                response = res[0]
                current = response.Current()
                current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
                print(res)
                print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
                print(f"Elevation {response.Elevation()} m asl")
                print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
                print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
                print(Variable.apparent_temperature)
                current_apparent_temperature = next(filter(lambda x: x.Variable() == Variable.apparent_temperature, current_variables))
                print(f"Variables : {current_variables} ")
                current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
                print(f"Current apparent temperature: {current_apparent_temperature.Value()}°C")
                return "ok"

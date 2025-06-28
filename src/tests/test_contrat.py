"""
Phase 3 : Tests de contrat
3.1 Validation des schémas JSON
Définir et implémenter des schémas de validation pour : 
- Structure des réponses API avec propriétés requises et optionnelles 
- Types de données et formats (nombres, chaînes, dates) 
- Contraintes de validation (énumérations, plages de valeurs) 
- Gestion des propriétés imbriquées (température, conditions météo)

Exemple de schéma simplifié :

const weatherSchema = {
  type: 'object',
  required: ['city', 'temperature'],
  properties: {
    city: { type: 'string' },
    temperature: {
      type: 'object',
      required: ['current']
      // À compléter...
    }
  }
};
Faites le votre ici
3.2 Tests de contrat avec les APIs externes
Mock des réponses des APIs tierces
Tests de robustesse en cas de changement de format
Validation des transformations de données
"""
import os
import sys
import httpx
import pytest
import dotenv
import datetime
from fastapi.testclient import TestClient
from jsonschema import validate, ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append("..") 
from src.services.api_fastapi.main import app
from src.models.response_models import OpenMeteoResponseModel, WeatherAPIResponseModel


dotenv.load_dotenv()

FASTAPI_HOST = os.getenv("fastapi_host", "")
FASTAPI_PORT = int(os.getenv("fastapi_port", 8000))
WEATHER_API_KEY = os.getenv("api_key_weather_api", "")
OPENWEATHER_API_KEY = os.getenv("api_key_open_weather", "")

# utils functions ------------------
def flatten(d):
    _d = dict()
    for k,v in d.items():
        if isinstance(v, dict):
            for vk, vv in v.items():
                _d[f"{k}/{vk}"] = vv
        else:
            _d[k] = v
    return _d

def call_api(test_client, api_name, city_name):
    """
    Appelle l'API spécifiée avec le nom de la ville.
    """
    response = test_client.get(f"/meteo/current/{api_name}/?city_name={city_name}")
    return response.json()

def validate_response(response, schema):
    """
    Valide la réponse de l'API contre le schéma spécifié.
    """
    try:
        validate(instance=response, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False


# tests de contrat ------------------
@pytest.fixture(scope="module")
def api_client_test():
    return TestClient(app)

def test_api_contract_output(api_client_test):
    """
    Test de contrat pour les APIs météo.
    Vérifie que les réponses des APIs respectent les schémas définis.
    """
    # appel API et vérification du schéma
    response = call_api(api_client_test, "openmeteo", "Paris")
    assert validate_response(response, OpenMeteoResponseModel.model_json_schema())

    response = call_api(api_client_test, "weatherapi", "Paris")
    assert validate_response(response, WeatherAPIResponseModel.model_json_schema())

@pytest.mark.parametrize(
  "apisourcename, apisourceroutetocall, cityname, apirequiredfieldsnames",
  [
    (
      "weatherapi",
      lambda cityname: f"https://api.weatherapi.com/v1/current.json?q={cityname}&key={WEATHER_API_KEY}",
      "Paris",
      {
        "location/lon": {"type": float},
        "location/lat": {"type": float},
        "location/localtime": {"type": str, "format": "datetime"},
        "current/temp_c": {"type": float, "min": -100, "max": 100},
        "current/feelslike_c": {"type": float, "min": -100, "max": 100},
        "current/humidity": {"type": int, "min": 0, "max": 100},
        "current/pressure_mb": {"type": float, "min": 0, "max": 2000},
        "current/vis_km": {"type": float, "min": 0, "max": 100},
        "current/wind_kph": {"type": float, "min": 0, "max": 200},
      }
    ),
    (
        "openwather",
        lambda cityname: f"http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit=1&appid={OPENWEATHER_API_KEY}",
        "Paris",
        {
            "name": {"type": str},
            "lat": {"type": float},
            "lon": {"type": float},
            "country": {"type": str},
            "state": {"type": str}
        }
    )
  ]
)
def test_api_contract_input(
    apisourcename, 
    apisourceroutetocall, 
    cityname, 
    apirequiredfieldsnames
    ):
    """
    Test de contrat pour les APIs météo.
    Vérifie que les réponses des APIs respectent les schémas définis.
    """
    # appel de l'API
    response = httpx.get(apisourceroutetocall(cityname))
    # vérification du statut de la réponse
    assert response.status_code == 200, f"API {apisourcename} returned status code {response.status_code}"
    # vérification du contenu de la réponse
    data = response.json()
    if isinstance(data, list):
        assert len(data) > 0, f"API {apisourcename} returned an empty list"
        data = data[0]
    data = flatten(data)
    
    for field, constraints in apirequiredfieldsnames.items():
        assert field in data, f"Field '{field}' is missing in the response from {apisourcename}"
        assert isinstance(data[field], constraints["type"]), f"Field '{field}' should be of type {constraints['type'].__name__} in {apisourcename}"
        
        if "min" in constraints:
            assert data[field] >= constraints["min"], f"Field '{field}' should be at least {constraints['min']} in {apisourcename}"
        if "max" in constraints:
            assert data[field] <= constraints["max"], f"Field '{field}' should be at most {constraints['max']} in {apisourcename}"
        if "format" in constraints and constraints["format"] == "datetime":
            try:
                datetime.datetime.fromisoformat(data[field])
            except ValueError:
                assert False, f"Field '{field}' should be a valid date-time format in {apisourcename}"

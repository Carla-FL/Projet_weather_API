from pydantic import BaseModel
from typing import Optional
from typing import Optional, List

single_source_model_rep = {
    "source": "",
    "localisation": {
        "longitude": "",
        "latitude": "",
        "pays": "",
        "ville": ""
    },
    "informations_temporelles": {
        "current_time": ""
    },
    "temperature": {
        "actuelle": "",
        "ressentie": "",
        "min": "",
        "max": "",
        "unité": ""
    },
    "conditions_meteorologiques": {
        "etat": "",
        "description": "",
        "humidité": "",
        "pression": "",
        "visibilité": ""
    },
    "vent": {
        "vitesse": "",
        "direction": "",
        "unité": ""
    }
}
class Localisation(BaseModel):
    longitude: Optional[str] = ""
    latitude: Optional[str] = ""
    pays: Optional[str] = ""
    ville: Optional[str] = ""

class InformationsTemporelles(BaseModel):
    current_time: Optional[str] = ""

class Temperature(BaseModel):
    actuelle: Optional[str] = ""
    ressentie: Optional[str] = ""
    min: Optional[str] = ""
    max: Optional[str] = ""
    unité: Optional[str] = ""

class ConditionsMeteorologiques(BaseModel):
    etat: Optional[str] = ""
    description: Optional[str] = ""
    humidité: Optional[str] = ""
    pression: Optional[str] = ""
    visibilité: Optional[str] = ""

class Vent(BaseModel):
    vitesse: Optional[str] = ""
    direction: Optional[str] = ""
    unité: Optional[str] = ""

class SingleSourceModelRep(BaseModel):
    source: Optional[str] = ""
    localisation: Optional[Localisation] = ""
    informations_temporelles: Optional[InformationsTemporelles] = ""
    temperature: Optional[Temperature] = ""
    conditions_meteorologiques: Optional[ConditionsMeteorologiques] = ""
    vent: Optional[Vent] = ""

class MultiSourceModelRep(BaseModel):
    data: List[SingleSourceModelRep]

class OpenMeteoResponseModel(SingleSourceModelRep):
    source: str = "openmeteo"
    localisation: Localisation
    informations_temporelles: InformationsTemporelles
    temperature: Temperature
    conditions_meteorologiques: ConditionsMeteorologiques
    vent: Vent

class WeatherAPIResponseModel(SingleSourceModelRep):
    source: str = "weatherapi"
    localisation: Localisation
    informations_temporelles: InformationsTemporelles
    temperature: Temperature
    conditions_meteorologiques: ConditionsMeteorologiques
    vent: Vent
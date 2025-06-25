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
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    pays: Optional[str] = None
    ville: Optional[str] = None

class InformationsTemporelles(BaseModel):
    current_time: Optional[str] = None

class Temperature(BaseModel):
    actuelle: Optional[str] = None
    ressentie: Optional[str] = None
    min: Optional[str] = None
    max: Optional[str] = None
    unité: Optional[str] = None

class ConditionsMeteorologiques(BaseModel):
    etat: Optional[str] = None
    description: Optional[str] = None
    humidité: Optional[str] = None
    pression: Optional[str] = None
    visibilité: Optional[str] = None

class Vent(BaseModel):
    vitesse: Optional[str] = None
    direction: Optional[str] = None
    unité: Optional[str] = None

class SingleSourceModelRep(BaseModel):
    source: Optional[str] = None
    localisation: Optional[Localisation] = None
    informations_temporelles: Optional[InformationsTemporelles] = None
    temperature: Optional[Temperature] = None
    conditions_meteorologiques: Optional[ConditionsMeteorologiques] = None
    vent: Optional[Vent] = None

class MultiSourceModelRep(BaseModel):
    data: List[SingleSourceModelRep]

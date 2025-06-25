from src.models.response_models import (
    MultiSourceModelRep, 
    SingleSourceModelRep
)

def get_multisource_meteo(city_name) -> MultiSourceModelRep:

    res_openmeteo: SingleSourceModelRep = SingleSourceModelRep() # openmeteo.get_meteo()
    res_openmeteo.source = "openmeteo"

    res_openweather: SingleSourceModelRep = SingleSourceModelRep() # openweather.get_meteo()
    res_openweather.source = "openweather"

    return MultiSourceModelRep(
        data = [
            res_openmeteo, 
            res_openweather
        ]
    )
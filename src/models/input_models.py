from typing import Optional
from pydantic import BaseModel


class OpenWeatherGeocodingModel(BaseModel):
    name : Optional[str] = ""
    lat: float
    lon: float
    country : Optional[str] = ""
    state : Optional[str] = ""


class OpenWeatherAPIResponseModel(BaseModel):
    temp : float
    feels_like : float
    pressure : int
    humidity : int
    dew_point : float
    uvi : float
    clouds : int
    visibility : int
    wind_speed : float
    wind_deg : int
# a incrementer si besoin avec d'autres chmaps 

class OpenMeteoAPIResponseModel(BaseModel):
    pass

class WeatherAPIResponseModel(BaseModel):
    pass

from pydantic import BaseModel


class OpenWeatherGeocodingModel(BaseModel):
    lat: float
    lon: float

class OpenWeatherAPIResponseModel(BaseModel):
    pass

class OpenMeteoAPIResponseModel(BaseModel):
    pass

class WeatherAPIResponseModel(BaseModel):
    pass

import os
import redis
import dotenv
import datetime
from .openmeteo import get_weather_from_openmeteo
from .openweather import get_weather_from_openweather
from .weatherapi import get_weather_from_weatherapi
from src.models.response_models import (
    MultiSourceModelRep, 
    SingleSourceModelRep
)

dotenv.load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("redis_host"), 
    port=int(os.getenv("redis_port")), 
    db=int(os.getenv("redis_db")))

def flatten(d):
    _d = dict()
    for k,v in d.items():
        if isinstance(v, dict):
            for vk, vv in v.items():
                _d[f"{k}/{vk}"] = vv
        else:
            _d[k] = v
    return _d

def make_redis_key(city_name):
    return f"weather:{city_name}" # composer avec la ville, le pays etc..

def call_multisource_meteo(city_name) -> MultiSourceModelRep:

    res_openmeteo: SingleSourceModelRep = get_weather_from_openmeteo(city_name)
    res_openweather: SingleSourceModelRep = get_weather_from_openweather(city_name)
    res_weatherapi: SingleSourceModelRep = get_weather_from_weatherapi(city_name)

    return MultiSourceModelRep(
        data = [
            res_openmeteo, 
            res_openweather,
            res_weatherapi
        ]
    )

def get_multisource_meteo(city_name): 
    """
    Implémente la facade avec redis.
    Quand on a une requete entrante, on regarde l'index redis
    Si existe, on prend le res sinon on appelle la fonction et
    on savaugarde sur redis.
    """
    s = datetime.datetime.now()
    redis_key = make_redis_key(city_name)    
    if redis_client.exists(redis_key):
        # si existe, récupère le cache
        print("cache hit for city:", city_name)
        res = redis_client.hgetall(redis_key)
        res = {k.decode(): eval(v.decode()) for k, v in res.items()}
    else:
        print("cache miss for city:", city_name)
        # retourne un modele à dumper pour obtenir un dict
        res = call_multisource_meteo(city_name).model_dump()
        # on convertit le dict en bytes et on enregistre dans le cache
        redis_client.hset(
            name=redis_key, 
            key="current_weather", 
            value=str(res).encode())
        # on a joute une limite de 10min pour le cache
        redis_client.expire(redis_key, 60*60) # 1h

    # on ajoute le temps de réponse de l'api
    res["rep_duration"] = f"{(datetime.datetime.now() - s).total_seconds() * 1000:.2f} ms"
    return res

import os
import redis
import dotenv
import datetime
from .openmeteo import get_weather_from_openmeteo
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
    return f"weather:current:{city_name}" # composer avec la ville, le pays etc..

def call_multisource_meteo(city_name) -> MultiSourceModelRep:

    res_openmeteo: SingleSourceModelRep = get_weather_from_openmeteo(city_name)

    res_openweather: SingleSourceModelRep = SingleSourceModelRep() # openweather.get_meteo()
    res_openweather.source = "openweather"

    return MultiSourceModelRep(
        data = [
            res_openmeteo, 
            res_openweather
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
        res = redis_client.hgetall(redis_key).items().decode()
        clean_redis_cache_after_hits(city_name, max_hits=3)
    else:
        print("cache miss for city:", city_name)
        # retourne un modele à dumper pour obtenir un dict
        res = call_multisource_meteo(city_name).model_dump()
        # on convertit le dict en bytes et on enregistre dans le cache
        redis_client.hset(name="myhash", key=redis_key, value=str(res).encode())
    # on ajoute le temps de réponse de l'api
    res["rep_duration"] = f"{(datetime.datetime.now() - s).total_seconds() * 1000:.2f} ms"
    return res


def clean_redis_cache_after_time(city_name, max_seconds=3600):
    redis_key = make_redis_key(city_name)
    timestamp_key = f"{redis_key}:timestamp"

    # Get the timestamp when the value was stored
    stored_timestamp = redis_client.get(timestamp_key)

    if stored_timestamp:
        stored_time = datetime.datetime.fromtimestamp(float(stored_timestamp))
        elapsed_time = (datetime.datetime.now() - stored_time).total_seconds()

        # Check if elapsed time exceeds max_seconds
        if elapsed_time > max_seconds:
            redis_client.delete(redis_key)
            redis_client.delete(timestamp_key)
    else:
        # Save the current timestamp if not already stored
        redis_client.set(timestamp_key, datetime.datetime.now().timestamp())


def clean_redis_cache_after_hits(city_name, max_hits=3):
    redis_key = make_redis_key(city_name)
    hit_count_key = f"{redis_key}:hits"
    print("evaluating redis cache for city:", city_name)
    # Increment hit count
    hit_count = redis_client.incr(hit_count_key)
    print(f"hit count for {city_name}: {hit_count}")
    # Check if hit count exceeds max_hits
    if hit_count > max_hits:
        redis_client.delete(redis_key)
        redis_client.delete(hit_count_key)
        print(f"cache reseted for : {city_name} after {hit_count} hits")
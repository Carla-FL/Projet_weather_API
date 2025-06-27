import dotenv, os

dotenv.load_dotenv()

FASTAPI_HOST = os.getenv("fastapi_host", "")
FASTAPI_PORT = int(os.getenv("fastapi_port", 8000))
    
if (not FASTAPI_HOST) or (not FASTAPI_PORT):
    raise ValueError("FASTAPI environment variables are not set correctly. Please set fastapi_host and fastapi_port in your .env file.")


class LoadTestConfig:
    # URLs de test
    BASE_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}"
    
    # Profils de charge
    LIGHT_LOAD = {
        "users": 10,
        "spawn_rate": 2,
        "duration": "2m"
    }
    
    NORMAL_LOAD = {
        "users": 50,
        "spawn_rate": 5,
        "duration": "10m"
    }
    
    STRESS_LOAD = {
        "users": 200,
        "spawn_rate": 10,
        "duration": "15m"
    }
    
    # Villes pour les tests
    CITIES = [
        "Paris", "London", "Berlin", "Madrid", "Rome",
        "Tokyo", "Sydney", "New York", "Los Angeles"
    ]
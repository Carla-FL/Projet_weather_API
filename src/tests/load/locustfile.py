import random
from locust import HttpUser, task, between


class WeatherAPIUser(HttpUser):
    # Temps d'attente entre les requêtes (1 à 5 secondes)
    wait_time = between(1, 5)
    
    def on_start(self):
        "Exécuté au démarrage de chaque utilisateur"
        # Initialisation si nécessaire (login, setup, etc.)
        pass
    
    @task(3)  # Poids 3 : cette tâche sera exécutée 3x plus souvent
    def get_current_weather(self):
        "Test de l'endpoint météo actuelle"
        cities = ["Paris", "London", "Tokyo", "New York", "Berlin"]
        city = random.choice(cities)
        with self.client.get(f"/meteo/current/?city_name={city}", 
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)  # Poids 2
    def get_weather_forecast(self):
        "Test de l'endpoint prévisions"
        cities = ["Paris", "Madrid", "Rome"]
        city = random.choice(cities)
        
        self.client.get(f"/meteo/forecast/?city_name={city}")
    
    @task(1)  # Poids 1 : moins fréquent
    def get_weather_history(self):
        "Test de l'endpoint historique"
        self.client.get("/meteo/history/?city_name=Paris?days=7")
    
    @task(1)
    def health_check(self):
        "Vérification de santé de l'API"
        self.client.get("/health")
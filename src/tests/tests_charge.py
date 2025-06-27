"""
Phase 4 : Tests de charge avec Locust
Qu'est-ce que Locust ?
Locust est un outil de test de charge open-source écrit en Python qui permet de simuler des milliers d'utilisateurs simultanés sur votre application. Contrairement à d'autres outils, Locust utilise du code Python pour définir le comportement des utilisateurs, ce qui le rend très flexible et expressif.

Avantages de Locust : - Scriptable : Définition des tests en Python (facile à comprendre et maintenir) - Distribué : Peut répartir la charge sur plusieurs machines - Interface web : Dashboard en temps réel pour monitoring - Flexible : Simulation de comportements utilisateur complexes - Extensible : Intégration facile avec d'autres outils

4.1 Installation et configuration Locust
Installation
pip install locust
Structure des fichiers de test
tests/load/
├── locustfile.py          # Fichier principal
├── weather_tasks.py       # Tâches spécifiques météo
└── config.py             # Configuration des tests
4.2 Configuration des tests de charge
Fichier principal (locustfile.py)
from locust import HttpUser, task, between
import random

class WeatherAPIUser(HttpUser):
    # Temps d'attente entre les requêtes (1 à 3 secondes)
    wait_time = between(1, 3)
    
    def on_start(self):
        "Exécuté au démarrage de chaque utilisateur"
        # Initialisation si nécessaire (login, setup, etc.)
        pass
    
    @task(3)  # Poids 3 : cette tâche sera exécutée 3x plus souvent
    def get_current_weather(self):
        "Test de l'endpoint météo actuelle"
        cities = ["Paris", "London", "Tokyo", "New York", "Berlin"]
        city = random.choice(cities)
        
        with self.client.get(f"/weather/current/{city}", 
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
        
        self.client.get(f"/weather/forecast/{city}")
    
    @task(1)  # Poids 1 : moins fréquent
    def get_weather_history(self):
        "Test de l'endpoint historique"
        self.client.get("/weather/history/Paris?days=7")
    
    @task(1)
    def health_check(self):
        "Vérification de santé de l'API"
        self.client.get("/health")
Configuration avancée
# config.py
class LoadTestConfig:
    # URLs de test
    BASE_URL = "http://localhost:3000"
    
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
4.3 Exécution des tests
Commandes de base
# Test interactif avec interface web
locust -f locustfile.py --host=http://localhost:3000

# Test en ligne de commande
locust -f locustfile.py --host=http://localhost:3000 \
       --users 50 --spawn-rate 5 --run-time 10m --headless

# Test avec rapport HTML
locust -f locustfile.py --host=http://localhost:3000 \
       --users 100 --spawn-rate 10 --run-time 5m \
       --headless --html=report.html

       
       
Test distribué (plusieurs machines) à titre de compréhension
# Machine maître
locust -f locustfile.py --master --host=http://localhost:3000

# Machines esclaves
locust -f locustfile.py --worker --master-host=192.168.1.100


4.4 Scénarios de test avancés
Test de montée en charge progressive
# scenarios.py
from locust import HttpUser, task, between
import logging

class RampUpTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def weather_scenario(self):
        "Scénario réaliste d'utilisation"
        # 1. Consultation météo actuelle
        response = self.client.get("/weather/current/Paris")
        
        if response.status_code == 200:
            # 2. Si succès, consulter les prévisions
            self.client.get("/weather/forecast/Paris")
            
            # 3. Parfois consulter l'historique (10% des cas)
            if random.random() < 0.1:
                self.client.get("/weather/history/Paris?days=3")

    ### Terminer le par vous même et faites votre propre scénario###
Validation des réponses

class WeatherAPIUser(HttpUser):
    @task
    def validate_weather_response(self):
        with self.client.get("/weather/current/Paris", 
                           catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status code: {response.status_code}")
            else:
                try:
                    data = response.json()
                    # Validation de la structure
                    if 'city' not in data or 'temperature' not in data:
                        response.failure("Missing required fields")
                    elif data['city'] != 'Paris':
                        response.failure("Wrong city in response")
                    else:
                        response.success()
                except Exception as e:
                    response.failure(f"Invalid JSON: {e}")
"""
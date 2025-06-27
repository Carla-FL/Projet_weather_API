from locust import HttpUser, task, between
import logging, random

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

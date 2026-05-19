from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Temps d'attente entre 1 et 3 secondes entre les tâches, simule temps de réflexion
    wait_time = between(1, 3)

    @task(2)
    def load_home(self):
        # Exemple : accéder à la page d'accueil / résumé, temps max 5s
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(f"Loading too slow: {response.elapsed.total_seconds()}s")
            else:
                response.success()

    @task(1)
    def purchase_places(self):
        # Exemple d'achat places avec POST, temps max 2s
        data = {
            "club": "Simply Lift",
            "competition": "Winter Wonderland",
            "places": "1"
        }
        with self.client.post("/purchasePlaces", data=data, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Purchase too slow: {response.elapsed.total_seconds()}s")
            else:
                response.success()
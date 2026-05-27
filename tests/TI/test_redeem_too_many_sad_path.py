import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_purchase_places_exceeds_points(client):
    # Données de test
    club_name = "Iron Temple"  # a 4 points
    competition_name = "Fall Classic"  # 13 places disponibles
    places_to_book = 10  # Supérieur aux points du club => bug reproduit
    
    # Simule un POST vers /purchasePlaces
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': places_to_book
    }, follow_redirects=True)
    
    # On vérifie que le message d'erreur est présent dans la réponse
    assert b'Error: You cannot use more points than you have.' in response.data
    
    # On peut aussi vérifier que les points et places n'ont pas changé (optionnel)
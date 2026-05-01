import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_purchase_places_happy_path(client):
    club_name = "Iron Temple"  # 4 points disponibles
    competition_name = "Spring Festival"  # 25 places disponibles
    places_to_book = 3  # Inférieur ou égal aux points du club
    
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': places_to_book
    }, follow_redirects=True)
    
    # Vérifie que la réservation a abouti (message de succès attendu)
    assert b'Great-booking complete!' in response.data
    
    # Optionnel : vérifiez que le nombre de places de la compétition ait diminué correctement
    # et que les points du club soient mis à jour (cela nécessite accès aux données du serveur)
import pytest
from server import app

@pytest.fixture
def client():
    """
    Fixture pour créer un client Flask de test, utilisé pour simuler les requêtes HTTP.
    """
    with app.test_client() as client:
        yield client

def test_integration_email_known_and_reservation_points_limit(client):
    """
    Test d'intégration minimal qui :
    - connecte un club connu ("Simply Lift") via son email,
    - tente une réservation dépassant les points disponibles (13 points),
      pour vérifier que la limite est respectée.
    """
    # Étape 1 : connexion avec email connu
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert b"Welcome" in response.data, "La connexion avec un email valide doit réussir."

    # Étape 2 : réservation trop importante (100 places alors que club a 13 points)
    reservation_data = {
        'competition': 'Winter Wonderland',
        'club': 'Simply Lift',
        'places': '100'  # valeur bien au-dessus des points disponibles
    }
    response = client.post('/purchasePlaces', data=reservation_data, follow_redirects=True)

    # Vérification que la réservation n'a pas réussi (pas de message de succès)
    assert b"Great-booking complete!" not in response.data, "La réservation dépasse les points et doit être refusée."

    # Optionnel : vérifier un message d'erreur adapté (si présent dans votre app)
    # assert b"not enough points" in response.data.lower()  # adapter si message exact connu
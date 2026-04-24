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


def test_integration_competition_places_limit(client):
    """
    Test d'intégration pour vérifier la gestion de la limite du nombre de places disponibles 
    dans la compétition "Winter Wonderland".
    
    Le test essaie de réserver plus de places que celles disponibles pour la compétition,
    et vérifie que la réservation est refusée.
    """
    # Connexion avec email valide
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert b"Welcome" in response.data, "La connexion avec un email valide doit réussir."

    # Tentative de réservation dépassant le nombre de places disponibles (ici 14 alors que 13 sont dispos)
    reservation_data = {
        'competition': 'Winter Wonderland',
        'club': 'Simply Lift',
        'places': '14'  # dépasse la limite de places disponibles
    }
    response = client.post('/purchasePlaces', data=reservation_data, follow_redirects=True)

    # Vérifier que la réservation n’a pas fonctionné (pas de message succès)
    assert b"Great-booking complete!" not in response.data, "Réservation dépassant les places doit être refusée."


def test_integration_club_places_limit(client):
    """
    Test d'intégration qui vérifie que la réservation ne peut pas dépasser
    la limite max de 12 places par club pour une compétition.
    """
    # Connexion avec email valide
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert b"Welcome" in response.data, "La connexion avec un email valide doit réussir."

    # Tentative de réservation dépassant la limite de 12 places par club (ici 13)
    reservation_data = {
        'competition': 'Winter Wonderland',
        'club': 'Simply Lift',
        'places': '13'  # dépasse la limite de 12
    }
    response = client.post('/purchasePlaces', data=reservation_data, follow_redirects=True)

    # Vérification que la réservation est refusée
    assert b"Great-booking complete!" not in response.data, "Réservation dépassant la limite de 12 places doit être refusée."
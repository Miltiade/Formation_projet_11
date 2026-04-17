import pytest
from server import app
from server import app, clubs, competitions

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_points_not_deducted_after_booking(client):
    club_name = 'Simply Lift'
    competition_name = 'Spring Festival'
    places_to_book = '2'

    # Récupération des points initiaux du club
    club = [c for c in clubs if c['name'] == club_name][0]
    initial_points = int(club['points'])

    # Effectuer la réservation (POST)
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': places_to_book
    }, follow_redirects=True)

    # Vérification que la réservation a été effectuée (message succès)
    assert b'Great-booking complete!' in response.data

    # Recharger le club pour voir ses points après réservation
    club_after = [c for c in app.clubs if c['name'] == club_name][0]
    points_after = int(club_after['points'])

    # Test sad path : les points n’ont PAS changé -> bug confirmé
    assert points_after == initial_points
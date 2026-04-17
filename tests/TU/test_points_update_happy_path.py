import pytest
from server import app, clubs

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_points_deduction_after_booking(client):
    # Récupérer le club et points initiaux
    club_name = 'Simply Lift'
    competition_name = 'Winter Wonderland'
    places_to_book = '3'

    # Trouver les points initiaux du club
    club = [c for c in clubs if c['name'] == club_name][0]
    initial_points = int(club['points'])

    # Effectuer la réservation
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': places_to_book
    }, follow_redirects=True)

    # Vérifier le message de succès
    assert b'Great-booking complete!' in response.data

    # Vérifier que les points ont été déduits
    club_after = [c for c in clubs if c['name'] == club_name][0]
    expected_points = initial_points - int(places_to_book)
    assert int(club_after['points']) == expected_points
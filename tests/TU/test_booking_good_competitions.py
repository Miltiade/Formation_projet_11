import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_booking_future_competition(client):
    data = {
        'competition': 'Winter Wonderland',  # compétition dans le futur ou récente selon vos données
        'club': 'Simply Lift',
        'places': '2'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    # On vérifie que le message de succès est affiché
    assert b"Great-booking complete!" in response.data
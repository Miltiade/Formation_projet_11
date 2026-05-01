import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_reservation_above_12_places(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"You cannot book more than 12 places" in response.data or b"error" in response.data.lower()

def test_reservation_up_to_12_places(client):
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '12'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"Great-booking complete!" in response.data
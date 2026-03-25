import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_purchase_places_over_available(client):
    # Sad path : demande plus de places que dispo
    data = { # adapter selon données
        'competition': 'Spring Festival',  
        'club': 'Simply Lift',
        'places': '30'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"You cannot redeem more places than available" in response.data

def test_purchase_places_within_available(client):
    # Happy path : demande valide
    data = { # adapter selon données
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"Great-booking complete!" in response.data
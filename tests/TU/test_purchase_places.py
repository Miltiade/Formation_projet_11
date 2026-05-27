import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_purchase_places_over_available(client):
    # Sad path : demande plus de places que dispo
    data = { # adapter selon données
        'competition': 'Winter Wonderland',  
        'club': 'Simply Lift',
        'places': '3'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    print(response.data)
    assert b"You cannot redeem more places than available" in response.data

def test_purchase_places_within_available(client):
    # Happy path : demande valide
    data = { # adapter selon données
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    print(response.data)
    assert b"Great-booking complete!" in response.data
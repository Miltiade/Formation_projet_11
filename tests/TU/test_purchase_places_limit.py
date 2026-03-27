import pytest
from server import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
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
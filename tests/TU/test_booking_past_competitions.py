import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_booking_past_competition(client):
    data = {
        'competition': 'Spring Festival',  # compétition passée
        'club': 'Simply Lift',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    # On vérifie que le message d'erreur attendu est là (qui n'existe pas encore, donc test doit échouer)
    assert b"You cannot book places for past competitions" in response.data
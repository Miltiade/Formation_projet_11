import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_integration_issues_1_to_3(client):
    # Issue 1 : gestion erreur email inconnu via /showSummary
    
    response = client.post('/showSummary', data={'email': 'inconnu@exemple.com'}, follow_redirects=True)
    assert b"Sorry, that email wasn't found." in response.data
    
    # Issue 2 : limite d’utilisation des points (club demande plus que son solde)
    club_name = "Iron Temple"  # 4 points
    competition_name = "Spring Festival"  # 25 places
    
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': 10  # supérieur aux points dispo => bug reproduit
    }, follow_redirects=True)
    assert b'Error: You cannot use more points than you have.' in response.data

    # Issue 3 : demande plus de places que disponibles pour une compétition
    club_name = "Simply Lift"  # 13 points
    competition_name = "Spring Festival"  # 25 places disponibles
    
    # Ici, on demande 30 places, > 25 donc doit bloquer
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': 30
    }, follow_redirects=True)
    assert b"You cannot redeem more places than available" in response.data
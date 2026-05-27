import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # # Réinitialiser les données avant chaque test
    # global clubs, competitions
    # clubs[:] = [
    #     {"name":"Simply Lift", "email":"john@simplylift.co", "points":"100"},
    #     {"name":"Iron Temple", "email":"admin@irontemple.com", "points":"4"},
    #     {"name":"She Lifts", "email":"kate@shelifts.co.uk", "points":"12"}
    # ]
    # competitions[:] = [
    #     {"name":"Spring Festival", "date":"2020-03-27 10:00:00", "numberOfPlaces":"25"},
    #     {"name":"Fall Classic", "date":"2020-10-22 13:30:00", "numberOfPlaces":"13"},
    #     {"name":"Winter Wonderland", "date":"2026-12-22 11:00:00", "numberOfPlaces":"5"}
    # ]
    with app.test_client() as client:
        yield client

def test_integration_issues_1_to_3(client):
    # Issue 1 : gestion erreur email inconnu via /showSummary
    
    response = client.post('/showSummary', data={'email': 'inconnu@exemple.com'}, follow_redirects=True)    
    assert b"Sorry, that email was not found." in response.data
    
    # Issue 2 : limite d’utilisation des points (club demande plus que son solde)
    club_name = "Iron Temple"  # 4 points
    competition_name = "Winter Wonderland"  # 20 places
    
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': 10  # supérieur aux points dispo => bug reproduit
    }, follow_redirects=True)    
    assert b'Error: You cannot use more points than you have.' in response.data
    

    # Issue 3 : demande plus de places que disponibles pour une compétition
    club_name = "Simply Lift"  # 100 points
    competition_name = "Winter Wonderland"  # 5 places disponibles
    
    # Ici, on demande 6 places, > 5 donc doit bloquer
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': 6
    }, follow_redirects=True)
    print(response.data.decode())
    assert b"You cannot redeem more places than available" in response.data
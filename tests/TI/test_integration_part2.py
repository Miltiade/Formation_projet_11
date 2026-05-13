"""Test d'intégration 2:
Issue 4 (limite 12 places) : tenter de réserver > 12 places → vérifier flash / message d’erreur.
Issue 5 (réservation compétition passée) : réserver dans compétition datée avant aujourd’hui → message d’erreur.
Issue 6 (points mis à jour) : réserver N places → vérifier diminution correspondante des points du club.
Issue 7 (affichage points tous clubs) : une fois connecté, vérifier dans la page de résumé que les points des clubs sont affichés.
"""

import pytest
from server import app, clubs, competitions
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Réinitialiser données avant chaque test pour éviter "effets de bord"
    global clubs, competitions
    clubs[:] = [
        {"name":"Simply Lift", "email":"john@simplylift.co", "points":"100"},
        {"name":"Iron Temple", "email":"admin@irontemple.com", "points":"4"},
        {"name":"She Lifts", "email":"kate@shelifts.co.uk", "points":"12"}
    ]
    competitions[:] = [
        {"name":"Spring Festival", "date":"2020-03-27 10:00:00", "numberOfPlaces":"25"},
        {"name":"Fall Classic", "date":"2020-10-22 13:30:00", "numberOfPlaces":"13"},
        {"name":"Winter Wonderland", "date":"2026-12-22 11:00:00", "numberOfPlaces":"5"}
    ]
    with app.test_client() as client:
        yield client

def test_integration_issues_4_to_7(client):
    club_name = "Simply Lift"
    competition_past = "Spring Festival"          # date passée
    competition_future = "Winter Wonderland"      # date future
    # competition_normal = "Fall Classic"          

    # --- Issue 4 : réserver plus de 12 places ---
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_future,
        'places': '13'   # >12
    }, follow_redirects=True)
    assert b"You cannot book more than 12 places" in response.data

    # --- Issue 5 : réserver dans compétition passée ---
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_past,
        'places': '1'
    }, follow_redirects=True)
    assert b"You cannot book places for past competitions" in response.data

    # --- Issue 6 : vérifier déduction points après réservation ---
    # Points initiaux
    club = next(c for c in clubs if c['name'] == club_name)
    initial_points = int(club['points'])

    places_to_book = 3
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_future,
        'places': str(places_to_book)
    }, follow_redirects=True)
    assert b"Great-booking complete!" in response.data
    club_after = next(c for c in clubs if c['name'] == club_name)
    assert int(club_after['points']) == initial_points - places_to_book

    # --- Issue 7 : affichage solde des points de tous les clubs dans page de résumé ---
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    # On vérifie que le nom et le point de chaque club apparaissent dans la page
    for c in clubs:
        assert c['name'].encode() in response.data
        assert str(c['points']).encode() in response.data
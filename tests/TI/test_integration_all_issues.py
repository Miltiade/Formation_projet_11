import pytest
from server import app, clubs, competitions
from datetime import datetime

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

# Issue #1 : gestion erreur email inconnu
def test_handle_unknown_email_error(client):
    response = client.post('/showSummary', data={'email': 'unknown@example.com'}, follow_redirects=True)
    assert b"Sorry, that email was not found." in response.data

# Issue #2 : limiter usage points (ex: ne peut pas utiliser plus de points que le club possède)
def test_points_usage_limit(client):
    data = {
        'club': "Iron Temple",  # a seulement 4 points
        'competition': "Winter Wonderland",
        'places': '5'           # demande plus que ses points
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"Error: You cannot use more points than you have." in response.data

# Issue #282 : limiter réservations au nombre de places disponibles par compétition
def test_book_limit_competition_places(client):
    # tenter de réserver plus de places que dispo dans competition "Winter Wonderland" (has 1 place)
    data = {
        'club': "Simply Lift",
        'competition': "Winter Wonderland",
        'places': '6'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    expected_message = b"You cannot redeem more places than available"
    assert expected_message in response.data

# Issue #4 : ne pas réserver plus de 12 places par réservation
def test_limit_12_places_per_club(client):
    data = {
        'club': "Simply Lift",
        'competition': "Winter Wonderland",
        'places': '13'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"You cannot book more than 12 places" in response.data

# Issue #5 : ne pas réserver pour compétition passée
def test_booking_past_competitions(client):
    data = {
        'club': "Simply Lift",
        'competition': "Spring Festival",  # compétition passée
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"You cannot book places for past competitions" in response.data

# Issue #6 : mise à jour des points suite à réservation valide
def test_points_update_not_reflected(client):
    club_name = "Simply Lift"
    competition_name = "Winter Wonderland"
    places_to_book = 3

    club = next(c for c in clubs if c['name'] == club_name)
    initial_points = int(club['points'])

    data = {
        'club': club_name,
        'competition': competition_name,
        'places': str(places_to_book)
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert b"Great-booking complete!" in response.data

    club_after = next(c for c in clubs if c['name'] == club_name)
    assert int(club_after['points']) == initial_points - places_to_book

# Issue #7 : afficher le solde des points de tous les clubs après connexion
def test_points_display_board(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    for c in clubs:
        assert c['name'].encode() in response.data
        assert str(c['points']).encode() in response.data
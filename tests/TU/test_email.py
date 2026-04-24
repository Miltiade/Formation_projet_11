import pytest
from votre_module import find_club_by_email  # adaptez le nom réel

def test_find_club_by_email_connu():
    club = find_club_by_email("john@simplylift.co")
    assert club["name"] == "Simply Lift"

def test_find_club_by_email_inconnu():
    with pytest.raises(Exception):  # ou ajustez l'erreur attendue
        find_club_by_email("inconnu@exemple.com")
import pytest
from app_utils import find_club_by_email

def test_find_club_by_email_connu():
    club = find_club_by_email("john@simplylift.co")
    assert club["name"] == "Simply Lift"

def test_find_club_by_email_inconnu():
    with pytest.raises(Exception):
        find_club_by_email("inconnu@exemple.com")
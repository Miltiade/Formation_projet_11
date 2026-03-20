import pytest
from app_utils import find_club_by_email
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) # Ajoute le dossier racine au début des chemins de recherche modules

def test_find_club_par_email_valide():
    club = find_club_by_email("john@simplylift.co")
    assert club["name"] == "Simply Lift"

def test_find_club_par_email_invalide():
    with pytest.raises(ValueError):
        find_club_by_email("inconnu@exemple.com")
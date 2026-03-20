import json

def load_clubs():
    with open('clubs.json') as file:
        clubs = json.load(file)['clubs']
    return clubs

def find_club_by_email(email):
    clubs = load_clubs()
    matching = [club for club in clubs if club['email'] == email]
    if matching:
        return matching[0]
    else:
        raise ValueError("Email non trouvé")
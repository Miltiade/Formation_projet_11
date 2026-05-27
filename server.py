import json
from flask import Flask,render_template,request,redirect,flash,url_for
from app_utils import find_club_by_email
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = find_club_by_email(request.form['email'])
    except ValueError:
        flash("Sorry, that email was not found.")
        return redirect(url_for('index'))
    
    # Redirection vers la version GET avec club_name en paramètre d'URL
    return redirect(url_for('showSummary_get', club_name=club['name']))
    
# Route GET qui affiche la page de résumé après redirect_post et les actions POST
@app.route('/showSummary')
def showSummary_get():
    club_name = request.args.get('club_name')
    if not club_name:
        flash("Club data missing.")
        return redirect(url_for('index'))
    
    # Recherche club
    club = next((c for c in clubs if c['name'] == club_name), None)
    if not club:
        flash("Unknown club.")
        return redirect(url_for('index'))
    
    # Affiche la page avec clubs, compétitions, et flash messages
    return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        # Redirige vers showSummary GET avec paramètre club si possible
        if foundClub:
            return redirect(url_for('showSummary_get', club_name=foundClub['name']))
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    if not club or not competition:
        flash("Club or competition not found.")
        return redirect(url_for('index'))
    
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        flash("Invalid number of places.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    club_points = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])

    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    if competition_date < now:
        flash("You cannot book places for past competitions")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired > club_points:
        flash('Error: You cannot use more points than you have.')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    if placesRequired > 12:
        flash("You cannot book more than 12 places")
        return redirect(url_for('showSummary_get', club_name=club['name']))

    if placesRequired > availablePlaces:
        flash(f"You cannot redeem more places than available. You requested {placesRequired} but only {availablePlaces} are left.")
        return redirect(url_for('showSummary_get', club_name=club['name']))

    # Mise à jour des places et points du club
    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = club_points - placesRequired

    flash('Great-booking complete!')
    # Redirection vers la page de résumé qui affichera success et données mises à jour
    return redirect(url_for('showSummary_get', club_name=club['name']))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
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

    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])


    # Convertir la date de la compétition en datetime
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    # Bloquer si compétition passée
    if competition_date < now:
        flash("You cannot book places for past competitions")
        return render_template('booking.html', club=club, competition=competition)



    if placesRequired > club_points:
        flash('Error: You cannot use more points than you have.')
        return render_template('booking.html', club=club, competition=competition)


    if placesRequired > 12:
        flash("You cannot book more than 12 places")
        return render_template('welcome.html', club=club, competition=competition)
    

    # If user wants more places than are available: error message
    if placesRequired > availablePlaces:
        flash(f"You cannot redeem more places than available. You requested {placesRequired} but only {availablePlaces} are left.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Else: user can book places
    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = int(club['points']) - placesRequired # Update club's points balance



    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
from flask import Flask, render_template, session, request, jsonify
from datetime import timedelta
from Stats import stats_route
from Gezondheid import update_afstand_in_sessie
from Data import Data_route, Data_vrienden_route
import requests

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

# Cookie-configuratie
app.config['SESSION_COOKIE_DOMAIN'] = 'momanijero.ddns.net'  # Gebruik je domeinnaam
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_SECURE'] = False  # Zet op True als je HTTPS gebruikt
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# dit geeft de tijd
@app.template_filter('datetimeformat')
def datetimeformat(value):
    from datetime import datetime
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

# hiermee kunnen we kijken of de API key werkt als je hem invult.
# dit is niet te gebruiken voor websitegebruikers maar alleen voor ons om te testen
@app.route('/session_info')
def session_info():
    steam_id = session.get('steam_id', 'Niet gevonden')
    api_key = session.get('api_key', 'Niet gevonden')
    print(f"Steam ID: {steam_id}, API Key: {api_key}")
    return f"Steam ID: {steam_id}, API Key: {api_key}"

# route voor de homepagina
@app.route('/')
def home():
    return render_template('Home.html')

# dit is onze route voor de vriendepagina. eventueel veranderen we dit in iets anders
@app.route('/Vrienden.')
def Vrienden():
    return render_template('Vrienden.html')

# dit is onze route voor de community.
@app.route('/Community.')
def Community():
    return render_template('Community.html')

#dit is onze route voor de gezondheid
@app.route('/gezondheid', methods=['GET', 'POST'])
def Gezondheid():
    # Verwerken van POST-verzoeken van de afstandssensor
    if request.method == 'POST':
        print(f"[POST] Ontvangen cookies: {request.cookies}")
        json_data = request.get_json()
        print(f"Ontvangen POST-data: {json_data}")  # Debug-log
        response = update_afstand_in_sessie(json_data)  # Aanroepen van functie in Gezondheid.py
        session.permanent = True  # Maak sessie permanent
        print(f"[POST] Ontvangen cookies: {request.cookies}")
        print(f"[POST] Sessie-inhoud: {dict(session)}")
        print(f"Response van update_afstand_in_sessie: {response}")  # Debug-log
        if response["status"] == "success":
            print(f"Sessie-inhoud na POST: {dict(session)}")  # Debug-log
            return jsonify(response), 200
        else:
            return jsonify(response), 400

    # Verwerken van GET-verzoeken via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        afstand = session.get('afstand', 'Niet beschikbaar')  # Haal de waarde uit de sessie
        print(f"[GET-AJAX] Ontvangen cookies: {request.cookies}")
        print(f"[GET-AJAX] Sessie-inhoud: {dict(session)}")
        print(f"JSON Response afstand: {afstand}")  # Debug-log
        return jsonify(afstand=afstand)
    print(f"[GET] Ontvangen cookies: {request.cookies}")
    print(f"[GET] Sessie-inhoud: {dict(session)}")
    # Normale paginaweergave voor Gezondheid.html
    afstand = session.get('afstand', 'Niet beschikbaar')  # Haal de afstand uit de sessie
    today_playtime = session.get('today_playtime', 'Niet beschikbaar')  # Haal speeltijd op
    weekly_playtime = session.get('weekly_playtime', 'Niet beschikbaar')  # Haal speeltijd op

    print(f"Afstand: {afstand}, Today playtime: {today_playtime}, Weekly playtime: {weekly_playtime}")  # Debug-log

    return render_template(
        'Gezondheid.html',
        today_playtime=today_playtime,
        weekly_playtime=weekly_playtime,
        afstand=afstand
    )


@app.route('/Data/json', methods=['GET'])
def Data_json():
    game_names = session.get('game_names', [])

    # Als game_names leeg is, haal de gegevens opnieuw op
    if not game_names:
        print("Sessie leeg. Ophalen van gegevens...")
        Data_route()()  # Haal de gegevens op en vul de sessie
        game_names = session.get('game_names', [])

    return jsonify({"game_names": game_names})


@app.route('/Vrienden./json', methods=['GET'])
def Vrienden_json():
    vrienden_names = session.get('vrienden_names', [])
    vrienden_data = session.get('vrienden_data', [])

    # Als de sessie leeg is, haal de gegevens opnieuw op
    if not vrienden_names or not vrienden_data:
        print("Sessie leeg. Ophalen van vriendenlijst en schermtijd...")
        Data_vrienden_route()()  # Roep de functie aan die de sessie vult
        vrienden_names = session.get('vrienden_names', [])
        vrienden_data = session.get('vrienden_data', [])

    # Retourneer de JSON-respons
    return jsonify({
        "vrienden_names": vrienden_names,
        "vrienden_data": vrienden_data
    })



# Stats route
stats_route(app)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)





"""
Bronnen:
https://www.youtube.com/watch?v=jQjjqEjZK58


Install:
pip install requests
pip install Flask
pip install python-dotenv
pip install Pin
pip install neopixel
"""

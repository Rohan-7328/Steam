from flask import Flask, render_template, session, request, jsonify
from datetime import timedelta
from Stats import stats_route
from Gezondheid import update_afstand_in_sessie

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

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
        json_data = request.get_json()
        print(f"Ontvangen POST-data: {json_data}")  # Debug-log
        response = update_afstand_in_sessie(json_data)  # Aanroepen van functie in Gezondheid.py
        print(f"Response van update_afstand_in_sessie: {response}")  # Debug-log
        if response["status"] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400

    # Verwerken van GET-verzoeken via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        afstand = session.get('afstand', 'Niet beschikbaar')  # Haal de waarde uit de sessie
        print(f"JSON Response afstand: {afstand}")  # Debug-log
        return jsonify(afstand=afstand)

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




# Stats route
app.add_url_rule('/Stats', 'Stats', stats_route(), methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True)



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
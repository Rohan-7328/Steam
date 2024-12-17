from flask import Flask, render_template, session
from datetime import timedelta
from Stats import stats_route

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

# Custom datetime filter
@app.template_filter('datetimeformat')
def datetimeformat(value):
    from datetime import datetime
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

# Route om sessiegegevens op te halen
@app.route('/session_info')
def session_info():
    steam_id = session.get('steam_id', 'Niet gevonden')
    api_key = session.get('api_key', 'Niet gevonden')
    print(f"Steam ID: {steam_id}, API Key: {api_key}")
    return f"Steam ID: {steam_id}, API Key: {api_key}"

# Bestaande routes
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/Vrienden.')
def Vrienden():
    return render_template('Vrienden.html')

@app.route('/Community.')
def Community():
    return render_template('Community.html')

@app.route('/Gezondheid.')
def Gezondheid():

    today_playtime = session.get('today_playtime', 'Niet beschikbaar')
    weekly_playtime = session.get('weekly_playtime', 'Niet beschikbaar')

    return render_template('Gezondheid.html', today_playtime=today_playtime, weekly_playtime=weekly_playtime)


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
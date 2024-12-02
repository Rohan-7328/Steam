from flask import Flask, render_template, request, session
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "jouw_zeer_veilige_secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/Vrienden.')
def Vrienden():
    return render_template('Vrienden.html')


@app.route('/Community.')
def Community():
    return render_template('Community.html')


@app.route('/Stats', methods=['GET', 'POST'])
def Stats():
    if request.method == 'POST':
        steam_id = request.form['steam_id']
        api_key = request.form['api_key']
        session['steam_id'] = steam_id
        session['api_key'] = api_key

    steam_id = session.get('steam_id')
    api_key = session.get('api_key')

    if steam_id and api_key:
        # Haal algemene gegevens op
        summary_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
        response_summary = requests.get(summary_url)

        if response_summary.status_code == 200:
            player_info = response_summary.json()['response']['players'][0]

            # Haal speeltijdgegevens op
            games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&include_played_free_games=true"
            response_games = requests.get(games_url)

            if response_games.status_code == 200:
                games_data = response_games.json()['response']['games']

                # Bereken speeltijd vandaag en deze week (voorbeeld: CS:GO appid = 730)
                today_playtime = 0
                weekly_playtime = 0

                for game in games_data:
                    if 'playtime_2weeks' in game:
                        weekly_playtime += game['playtime_2weeks']  # Speeltijd in de afgelopen 2 weken (in minuten)
                        if game['appid'] == 730:  # Vervang dit met een specifieke game als nodig
                            today_playtime = game['playtime_forever'] - (weekly_playtime - game['playtime_2weeks'])

                # Zet speeltijd om naar uren en minuten
                today_hours = today_playtime // 60
                today_minutes = today_playtime % 60

                weekly_hours = weekly_playtime // 60
                weekly_minutes = weekly_playtime % 60

                return render_template(
                    'Stats.html',
                    player_info=player_info,
                    steam_id=steam_id,
                    api_key=api_key,
                    today_playtime=f"{today_hours} uur en {today_minutes} minuten",
                    weekly_playtime=f"{weekly_hours} uur en {weekly_minutes} minuten"
                )
            else:
                error_message = f"API-fout bij het ophalen van games: {response_games.status_code}"
                return render_template('Stats.html', error=error_message, steam_id=steam_id, api_key=api_key)
        else:
            error_message = f"API-fout bij het ophalen van gebruikersgegevens: {response_summary.status_code}"
            return render_template('Stats.html', error=error_message, steam_id=steam_id, api_key=api_key)

    return render_template('Stats.html', steam_id=steam_id, api_key=api_key)


@app.route('/Gezondheid.')
def Gezondheid():
    return render_template('Gezondheid.html')


if __name__ == '__main__':
    app.run(debug=True)
"""
Bronnen:
https://www.youtube.com/watch?v=jQjjqEjZK58


Install:
pip install requests
pip install Flask
pip install python-dotenv
"""
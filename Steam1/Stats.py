from flask import render_template, request, session
import requests
from Data import fetch_game_names  # Vervangt recommendations

# render_template: Hiermee wordt een HTML-bestand gerenderd en teruggestuurd naar de browser.
# request: hiermee kun je gegevens ophalen uit formulieren
# session: hiermee kan je tijdelijk gegevens opslaan waardoor je dus bijvoorbeeld makkelijk
# gegevens kan krijgen van Stats.py naar Gezondheid.py
# requests is een externe bibliotheek om HTTP verzoeken naar andere APIs te kunnen sturen

def stats_route(app):
    # stats_route() is de functie die flask gebruikt om de route /Stats te maken
    @app.route('/Stats', methods=['GET', 'POST'])
    # hiermee maak je het pad voor de site

    def Stats():
        # Stats() is de functie die die word doorgegeven aan flask
        if request.method == 'POST':
            # dit controleerd of het een POST verzoek is. dit word gebruikt
            # wanneer je gegevens naar de server stuurt

            session.clear()
            # reset de Flask sessie als je een nieuwe key invult
            steam_id = request.form['steam_id']
            api_key = request.form['api_key']
            # hiermee haal je de steamID en API key uit de HTML site

            # Hiermee sla je de key en ID op in een sessie
            session['steam_id'] = steam_id
            session['api_key'] = api_key

            # Dit verandert niks op de site maar dit is om te kijken
            # hoe de gegevens binnenkomen
            print(steam_id)
            print(api_key)

        steam_id = session.get('steam_id')
        api_key = session.get('api_key')
        # hier worden de waarden uit de sessie gehaald. als er niks word geretourneerd
        # dan komt er "Niet gevonden" op de site te staan

        if steam_id and api_key:
            # dit werkt alleen als er een Steam ID en API key zijn
            # als die er niet zijn dan werkt het dus ook niet
            try:
                summary_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
                # dit is de URL waarmee je spelergegevens ophaalt
                response_summary = requests.get(summary_url)
                # hiermee stuur je een GET verzoek naar de Steam-API
                response_summary.raise_for_status()
                # dit controleert of het succesvol was
                players = response_summary.json().get('response', {}).get('players', [])
                # response.json zet de API response om in een python dictionary
                # haalt een lijst van spelers uit de key

                if not players:
                    raise ValueError("Geen spelergegevens gevonden. Controleer je Steam ID of API-key.")
                # als er geen spelergegevens zijn dan komt er een foutmelding

                player_info = players[0]
                games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&include_played_free_games=true"
                # dit is de link om de speeltijd op te halen
                response_games = requests.get(games_url)
                response_games.raise_for_status()
                games_data = response_games.json().get('response', {}).get('games', [])
                # zet het om in een json formaat

                today_playtime = 0
                weekly_playtime = 0

                for game in games_data:
                    # dit loopt alle games van de speler door
                    if 'playtime_2weeks' in game:
                        weekly_playtime += game['playtime_2weeks']
                        # dit is voor de speeltijd van de afgelopen 2 weken

                today_hours = today_playtime // 60
                today_minutes = today_playtime % 60
                weekly_hours = weekly_playtime // 60
                weekly_minutes = weekly_playtime % 60
                # de speeltijd wordt hier omgerekend van minuten naar uren en minuten

                session['today_playtime'] = f"{today_hours} uur en {today_minutes} minuten"
                session['weekly_playtime'] = f"{weekly_hours} uur en {weekly_minutes} minuten"

                game_ids = [game.get('appid') for game in games_data]
                game_names = fetch_game_names(game_ids)  # Gebruik game_names in plaats van recommendations

                return render_template(
                    # hiermee wordt het HTML-bestand Stats.html weergegeven
                    'Stats.html',
                    player_info=player_info,
                    today_playtime=f"{today_hours} uur en {today_minutes} minuten",
                    weekly_playtime=f"{weekly_hours} uur en {weekly_minutes} minuten",
                    game_names=game_names  # Stuur game_names naar de HTML
                )

            except requests.exceptions.HTTPError as http_err:
                if http_err.response.status_code == 403:
                    error_message = "Onjuiste API-key ingevoerd. Controleer je API-key en probeer het opnieuw."
                else:
                    error_message = f"HTTP-fout: {http_err}"
                return render_template('Stats.html', error=error_message, steam_id=steam_id, api_key=api_key)
            except Exception as e:
                error_message = str(e)
                return render_template('Stats.html', error=error_message, steam_id=steam_id, api_key=api_key)

        # Render standaardpagina als er geen POST is of bij GET
        return render_template('Stats.html', steam_id=steam_id, api_key=api_key)

    return Stats

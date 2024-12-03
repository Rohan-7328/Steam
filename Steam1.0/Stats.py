from flask import render_template, request, session
import requests

def stats_route():
    def Stats():
        if request.method == 'POST':
            steam_id = request.form['steam_id']
            api_key = request.form['api_key']
            session['steam_id'] = steam_id
            session['api_key'] = api_key

        steam_id = session.get('steam_id')
        api_key = session.get('api_key')

        if steam_id and api_key:
            summary_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
            response_summary = requests.get(summary_url)

            if response_summary.status_code == 200:
                player_info = response_summary.json()['response']['players'][0]
                games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&include_played_free_games=true"
                response_games = requests.get(games_url)

                if response_games.status_code == 200:
                    games_data = response_games.json()['response']['games']
                    today_playtime = 0
                    weekly_playtime = 0

                    for game in games_data:
                        if 'playtime_2weeks' in game:
                            weekly_playtime += game['playtime_2weeks']
                            if game['appid'] == 730:
                                today_playtime = game['playtime_forever'] - (weekly_playtime - game['playtime_2weeks'])

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

    return Stats

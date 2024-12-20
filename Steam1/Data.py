import requests
from flask import session, jsonify


def fetch_game_names(game_ids):
    game_names = []
    for appid in game_ids:
        try:
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data[str(appid)].get("success"):
                game_name = data[str(appid)]["data"].get("name", "Onbekend")
                game_names.append({"id": appid, "name": game_name})
            else:
                game_names.append({"id": appid, "name": "Niet beschikbaar"})
        except Exception as e:
            game_names.append({"id": appid, "name": f"Fout: {str(e)}"})
    return game_names


def Data_route():
    def Data():
        api_key = session.get('api_key')
        steam_id = session.get('steam_id')

        if not api_key or not steam_id:
            return jsonify({"status": "error", "message": "API-key of Steam ID niet gevonden in de sessie."}), 400

        try:
            # Haal game-ID's op
            url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
            response = requests.get(url)
            response.raise_for_status()
            games_data = response.json().get('response', {}).get('games', [])

            if not games_data:
                return jsonify({"status": "error", "message": "Geen games gevonden voor deze gebruiker."}), 404

            game_ids = [game.get('appid') for game in games_data]
            session['game_ids'] = game_ids

            # Haal game-namen op
            game_names = fetch_game_names(game_ids)
            session['game_names'] = game_names

            return jsonify({"status": "success", "game_names": game_names}), 200
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "error", "message": f"Fout bij verbinding met Steam API: {str(e)}"}), 500

    return Data


def fetch_vrienden_namen(vrienden_ids):
    vrienden_namen = []
    for steamid in vrienden_ids:
        try:
            url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={session.get('api_key')}&steamids={steamid}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            players = data.get('response', {}).get('players', [])
            if players:
                player_name = players[0].get("personaname", "Onbekend")
                vrienden_namen.append({"id": steamid, "name": player_name})
            else:
                vrienden_namen.append({"id": steamid, "name": "Niet beschikbaar"})
        except Exception as e:
            vrienden_namen.append({"id": steamid, "name": f"Fout: {str(e)}"})
    return vrienden_namen

def Data_vrienden_route():
    def Data():
        api_key = session.get('api_key')
        steam_id = session.get('steam_id')

        if not api_key or not steam_id:
            return jsonify({"status": "error", "message": "API-key of Steam ID niet gevonden in de sessie."}), 400

        try:
            # Haal vriendenlijst op
            url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
            response = requests.get(url)
            response.raise_for_status()
            vrienden_data = response.json().get('friendslist', {}).get('friends', [])

            if not vrienden_data:
                return jsonify({"status": "error", "message": "Geen vrienden gevonden voor deze gebruiker."}), 404

            vrienden_ids = [vriend.get('steamid') for vriend in vrienden_data]
            session['vrienden_ids'] = vrienden_ids

            # Haal vrienden-namen op
            vrienden_names = fetch_vrienden_namen(vrienden_ids)
            session['vrienden_names'] = vrienden_names

            return jsonify({"status": "success", "vrienden_names": vrienden_names}), 200
        except requests.exceptions.RequestException as e:
            return jsonify({"status": "error", "message": f"Fout bij verbinding met Steam API: {str(e)}"}), 500

    return Data




from flask import session

def update_afstand_in_sessie(json_data):
    if json_data and 'distance' in json_data:
        afstand = json_data.get('distance')
        print(f"Ontvangen afstand: {afstand} cm")
        session['afstand'] = afstand  # Opslaan in sessie
        return {"status": "success", "afstand": afstand}
    else:
        print("Geen geldige data ontvangen")
        return {"status": "error", "message": "Geen geldige data ontvangen"}

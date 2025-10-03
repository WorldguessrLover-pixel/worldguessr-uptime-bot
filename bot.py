import os
import requests
import json
from flask import Flask
from storage import load_data, save_data
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, LEADERBOARD_URL

app = Flask(__name__)

# --- Fonction pour envoyer un message Telegram ---
def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    r = requests.post(url, data=data)
    print("[DEBUG] Envoi Telegram:", r.text)  # <-- pour debug Render logs


# --- Test automatique au lancement ---
def send_test_message():
    send_telegram_message("✅ Test automatique : le bot est bien connecté.")


# --- Fonction principale de vérification ---
def run_check():
    # Test Telegram au début
    send_test_message()

    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        leaderboard = response.json()
    except Exception as e:
        print(f"[ERREUR] Impossible de récupérer le leaderboard : {e}")
        return "Erreur lors de la récupération du leaderboard"

    old_data = load_data()
    new_data = {}

    changes = []
    for player in leaderboard:
        name = player.get("name")
        elo = player.get("elo")

        new_data[name] = elo

        old_elo = old_data.get(name)
        if old_elo is not None and elo != old_elo:
            diff = elo - old_elo
            changes.append(f"🔔 {name} a changé d'ELO: {old_elo} → {elo} ({'+' if diff > 0 else ''}{diff})")

    save_data(new_data)

    if changes:
        message = "\n".join(changes)
        send_telegram_message(message)
        return message
    else:
        return "Aucun changement détecté."


# --- Route Flask ---
@app.route("/")
def index():
    result = run_check()
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

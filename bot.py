import os
import requests
from flask import Flask
from storage.py import load_previous_data, save_current_data

# Variables d'environnement depuis Render
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
LEADERBOARD_URL = os.environ["LEADERBOARD_URL"]

app = Flask(__name__)

def send_message(text):
    """Envoie un message sur Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def run_check():
    """Récupère les données du leaderboard, compare et envoie les changements."""
    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        players = response.json()  # ← JSON est bien une liste de dicts

        previous_data = load_previous_data()
        current_data = {p["username"]: {"elo": p["elo"], "eloToday": p["eloToday"]} for p in players}

        # Compare avec la dernière exécution
        for username, data in current_data.items():
            old = previous_data.get(username)
            if old:
                if data["elo"] != old["elo"] or data["eloToday"] != old["eloToday"]:
                    send_message(
                        f"📊 {username} a changé :\n"
                        f"ELO: {old['elo']} → {data['elo']}\n"
                        f"ELO Today: {old['eloToday']} → {data['eloToday']}"
                    )
            else:
                send_message(f"🆕 Nouveau joueur détecté : {username} (ELO {data['elo']})")

        save_current_data(current_data)

    except Exception as e:
        send_message(f"❌ Erreur lors de la récupération du leaderboard: {e}")

@app.route("/", methods=["GET", "HEAD"])
def index():
    run_check()
    return "Bot is running!", 200


import os
import time
import requests
import json
from flask import Flask
from storage import load_data, save_data

# ===============================
# Config depuis les variables Render
# ===============================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
LEADERBOARD_URL = os.environ.get("LEADERBOARD_URL")

CHECK_INTERVAL = 300  # toutes les 5 minutes

# ===============================
# Flask pour Render
# ===============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running 🚀"

# ===============================
# Telegram
# ===============================
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur envoi Telegram: {e}")

# ===============================
# Leaderboard
# ===============================
def fetch_leaderboard():
    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur récupération leaderboard: {e}")
        return None

def check_updates():
    old_data = load_data()
    new_data = fetch_leaderboard()
    if not new_data:
        return

    for player in new_data.get("players", []):
        name = player["name"]
        elo = player["elo"]

        old_elo = old_data.get(name)
        if old_elo is not None and elo != old_elo:
            diff = elo - old_elo
            if abs(diff) >= 1:  # Seulement si variation
                send_message(f"🔥 {name} a changé d’ELO : {old_elo} ➝ {elo} ({'+' if diff > 0 else ''}{diff})")

        # Mise à jour sauvegarde
        old_data[name] = elo

    save_data(old_data)

# ===============================
# Boucle
# ===============================
def run_bot():
    while True:
        check_updates()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

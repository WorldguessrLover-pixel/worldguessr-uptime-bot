import requests
import time
import threading
import os
from storage import load_data, save_data

# Récupérer depuis les variables d'environnement Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")

# Fonction pour envoyer un message à Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erreur envoi Telegram:", e)

# Fonction qui check le leaderboard
def check_leaderboard():
    try:
        response = requests.get(LEADERBOARD_URL)
        leaderboard = response.json()

        players = []
        for player in leaderboard.get("players", []):
            players.append({
                "name": player.get("name"),
                "score": player.get("score")
            })

        # DEBUG : afficher les joueurs dans les logs Render
        print("=== DEBUG - Joueurs récupérés ===")
        print(players)

        # Sauvegarde des données (même si pas de changement)
        save_data({
            "last_check": time.strftime("%Y-%m-%d %H:%M:%S"),
            "players": players
        })

        # Exemple de notif si un joueur > 8000
        for p in players:
            if p["score"] >= 8000:
                send_telegram_message(f"🔥 {p['name']} est maintenant à {p['score']} ELO !")

    except Exception as e:
        print("Erreur dans check_leaderboard:", e)

# Lancer la vérif toutes les 5 minutes
def start_loop():
    while True:
        check_leaderboard()
        time.sleep(300)

# Lancer dans un thread
threading.Thread(target=start_loop, daemon=True).start()

# Flask pour que Render garde le service actif
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/show-logs')
def show_logs():
    data = load_data()
    if not data:
        return "storage.json n'existe pas encore."
    return data

import os
import time
import requests
import threading
import json
from flask import Flask

# Variables depuis Render (Dashboard > Environment)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")

STORAGE_FILE = "storage.json"

def save_data(data):
    """Sauvegarde toujours, même si data est vide"""
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ storage.json mis à jour")
    except Exception as e:
        print("❌ Erreur save_data:", e)

def load_data():
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print("📩 Message Telegram envoyé:", msg)
    except Exception as e:
        print("❌ Erreur Telegram:", e)

def check_leaderboard():
    try:
        response = requests.get(LEADERBOARD_URL)
        leaderboard = response.json()

        # DEBUG : afficher le JSON brut
        print("=== DEBUG JSON ===")
        print(leaderboard)

        players = []
        for player in leaderboard:
            players.append({
                "name": player.get("username"),
                "elo": player.get("elo")
            })

        data = {
            "last_check": time.strftime("%Y-%m-%d %H:%M:%S"),
            "players": players
        }

        save_data(data)

        for p in players:
            if p["elo"] >= 8000:
                send_telegram_message(f"🔥 {p['name']} est maintenant à {p['elo']} ELO !")

    except Exception as e:
        print("❌ Erreur check_leaderboard:", e)
        # Forcer quand même une sauvegarde vide
        save_data({"last_check": time.strftime("%Y-%m-%d %H:%M:%S"), "players": []})

def start_loop():
    while True:
        check_leaderboard()
        time.sleep(300)

# Lancer directement une première vérif
check_leaderboard()

threading.Thread(target=start_loop, daemon=True).start()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/show-logs')
def show_logs():
    return load_data()

import time
import requests
from flask import Flask
from storage import load_data, save_data
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, LEADERBOARD_URL

app = Flask(__name__)

def fetch_leaderboard():
    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erreur récupération leaderboard:", e)
        return None

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Message envoyé:", text, "| Réponse Telegram:", response.json())  # 👈 Debug
    except Exception as e:
        print("Erreur envoi Telegram:", e)

def check_updates():
    old_data = load_data()
    new_data = fetch_leaderboard()
    if not new_data:
        return

    for player in new_data.get("players", []):
        name = player["name"]
        elo = player["elo"]

        old_elo = old_data.get(name)
        print(f"DEBUG: {name} old={old_elo}, new={elo}")  # 👈 Debug affichage comparaison

        if old_elo is not None and elo != old_elo:
            diff = elo - old_elo
            if abs(diff) >= 1:
                send_message(
                    f"🔥 {name} a changé d’ELO : {old_elo} ➝ {elo} ({'+' if diff > 0 else ''}{diff})"
                )

        # Sauvegarde du nouvel ELO
        old_data[name] = elo

    save_data(old_data)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    while True:
        check_updates()
        time.sleep(300)  # toutes les 5 minutes

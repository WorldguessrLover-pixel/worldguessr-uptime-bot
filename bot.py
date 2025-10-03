import requests
import time
import json
import os
from flask import Flask
from storage import load_data, save_data

app = Flask(__name__)

STORAGE_FILE = "storage.json"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("Erreur lors de l'envoi du message Telegram:", response.text)
    except Exception as e:
        print("Exception lors de l'envoi Telegram:", str(e))

def check_leaderboard():
    try:
        response = requests.get(LEADERBOARD_URL)
        if response.status_code == 200:
            leaderboard = response.json()
            old_data = load_data()
            new_data = {}

            for player in leaderboard:
                name = player["name"]
                elo = player["elo"]
                new_data[name] = elo

                # Comparaison avec anciennes données
                if name in old_data:
                    old_elo = old_data[name]
                    if elo != old_elo:
                        diff = elo - old_elo
                        send_telegram_message(f"{name} a changé : {old_elo} → {elo} (diff: {diff})")
                else:
                    send_telegram_message(f"Nouveau joueur détecté: {name} avec {elo} Elo")

            save_data(new_data)
        else:
            print("Erreur récupération leaderboard:", response.status_code)
    except Exception as e:
        print("Exception lors du check leaderboard:", str(e))

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/show-logs")
def show_logs():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
        print("=== CONTENU storage.json ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("============================")
        return f"<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>"
    else:
        return "storage.json n'existe pas encore."

if __name__ == "__main__":
    # Lancer le bot + serveur Flask
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    def run_checker():
        while True:
            check_leaderboard()
            time.sleep(300)  # toutes les 5 minutes

    threading.Thread(target=run_flask).start()
    run_checker()

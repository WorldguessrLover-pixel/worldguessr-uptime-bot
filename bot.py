import time
import requests
from storage import load_data, save_data
from flask import Flask
import threading
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, LEADERBOARD_URL

app = Flask(__name__)

# Fonction pour envoyer un message test sur Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, json=payload)
        print("📨 Message Telegram envoyé:", r.json())
    except Exception as e:
        print("❌ Erreur envoi Telegram:", e)

# Fonction pour vérifier et simuler le leaderboard
def check_leaderboard():
    data = load_data()

    # 🔹 Test forcé : si le fichier est vide, on ajoute une entrée fictive
    if not data:
        print("⚡ Aucune donnée détectée, ajout d'une entrée fictive pour test...")
        data = {
            "last_check": time.strftime("%Y-%m-%d %H:%M:%S"),
            "players": [
                {"name": "TestUser", "score": 9999}
            ]
        }
        save_data(data)
        send_telegram_message("✅ Bot en ligne ! Données de test enregistrées.")
    else:
        print("📡 Données déjà présentes, pas besoin de test.")

    return data

# Tâche en arrière-plan
def run_checker():
    while True:
        check_leaderboard()
        time.sleep(60)  # vérifie toutes les 60 secondes

@app.route('/')
def home():
    return "Bot WorldGuessr est en ligne 🚀"

@app.route('/show-logs')
def show_logs():
    data = load_data()
    if not data:
        return "storage.json n'existe pas encore ou est vide."
    return str(data)

# Lancer le checker dans un thread parallèle
threading.Thread(target=run_checker, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

import os
import json
import requests
from flask import Flask
from storage import load_data, save_data

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LEADERBOARD_URL = "https://www.geoguessr.com/api/leaderboard"  # adapte si besoin


def send_telegram_message(message: str):
    """Envoie un message sur Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Erreur envoi Telegram:", e)


def fetch_leaderboard():
    """Récupère les données du leaderboard depuis l’API."""
    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erreur API:", response.status_code, response.text)
    except Exception as e:
        print("Erreur de requête:", e)
    return []


def run_check():
    """Compare les données actuelles avec celles stockées."""
    old_data = load_data()
    leaderboard = fetch_leaderboard()

    if not leaderboard:
        return

    new_data = {}
    for player in leaderboard:
        if isinstance(player, dict):  # sécurité
            name = player.get("name")
            rating = player.get("rating")

            if name and rating:
                old_rating = old_data.get(name)
                if old_rating is not None and rating != old_rating:
                    diff = rating - old_rating
                    message = f"{name} a changé d’elo : {old_rating} → {rating} ({diff:+})"
                    send_telegram_message(message)

                new_data[name] = rating

    save_data(new_data)


@app.route("/")
def index():
    run_check()
    return "OK", 200


# ✅ Route spéciale pour afficher storage.json dans les logs
@app.route("/show-logs")
def show_logs():
    data = load_data()
    print("=== CONTENU storage.json ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("============================")
    return "Données affichées dans les logs !", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

import os
import requests
from flask import Flask
from storage import load_data, save_data

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")


def send_telegram_message(message: str):
    """Envoie un message sur Telegram via l’API Bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur en envoyant le message Telegram: {e}")


def fetch_leaderboard():
    """Récupère le leaderboard depuis l’API."""
    response = requests.get(LEADERBOARD_URL)
    response.raise_for_status()
    return response.json()


def run_check():
    """Compare les ELO avec l’ancienne sauvegarde et envoie des notifs si ça change."""
    old_data = load_data()
    new_data = fetch_leaderboard()

    for player in new_data:
        name = player.get("name")
        elo = player.get("elo")

        if not name or elo is None:
            continue

        # Ancien score (None si joueur nouveau)
        old_elo = old_data.get(name)

        # Si nouveau joueur ou changement d’elo
        if old_elo is None or old_elo != elo:
            if elo >= 10000:
                message = f"⚠️ Le joueur {name} est maintenant à {elo} ELO (ancien: {old_elo})"
            elif elo >= 8000:
                message = f"Le joueur {name} est maintenant à {elo} ELO (ancien: {old_elo})"
            else:
                message = None

            if message:
                send_telegram_message(message)

        # Mise à jour dans la sauvegarde
        old_data[name] = elo

    save_data(old_data)


@app.route("/")
def index():
    """Point d’entrée appelé par UptimeRobot pour exécuter la vérification."""
    run_check()
    return "Leaderboard check executed!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

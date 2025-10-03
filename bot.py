import os
import requests
from flask import Flask
from storage import load_previous_data, save_current_data

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_URL = os.getenv("API_URL")

app = Flask(__name__)

def run_check():
    try:
        response = requests.get(API_URL)
        data = response.json()

        previous_data = load_previous_data()
        messages = []

        for player in data:
            username = player.get("username")
            elo_today = player.get("eloToday")

            if previous_data.get(username) != elo_today:
                messages.append(f"{username} a un nouvel eloToday : {elo_today}")

            previous_data[username] = elo_today

        save_current_data(previous_data)

        for msg in messages:
            send_telegram_message(msg)

    except Exception as e:
        send_telegram_message(f"Erreur dans run_check : {e}")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

@app.route("/")
def index():
    run_check()
    return "Bot en ligne ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render fournit $PORT automatiquement
    app.run(host="0.0.0.0", port=port)

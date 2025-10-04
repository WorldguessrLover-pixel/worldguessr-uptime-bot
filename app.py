from flask import Flask, jsonify
import threading
import time
import bot
import storage  # pour accéder à load_data()

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

# ➡️ Nouvelle route pour consulter les logs sauvegardés
@app.route("/show-logs")
def show_logs():
    data = storage.load_data()
    return jsonify(data)


def background_task():
    while True:
        try:
            print("🔄 Lancement du check du leaderboard...")
            bot.run_check()
        except Exception as e:
            print(f"❌ Erreur dans run_check : {e}")
        time.sleep(300)


def start_background():
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_background()
    app.run(host="0.0.0.0", port=10000)

from flask import Flask
import threading
import time
import bot  # ton bot.py

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200


def background_task():
    """Tâche en arrière-plan pour surveiller le leaderboard."""
    while True:
        try:
            print("🔄 Lancement du check du leaderboard...")
            bot.check_leaderboard()  # ✅ correction ici
        except Exception as e:
            print(f"❌ Erreur dans check_leaderboard : {e}")
        time.sleep(300)  # 5 min


def start_background():
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_background()
    app.run(host="0.0.0.0", port=10000)

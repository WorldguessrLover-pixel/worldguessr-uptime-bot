from flask import Flask
import threading
import bot  # ton script qui check le leaderboard et envoie à Telegram

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running ✅"

@app.route('/show-logs')
def show_logs():
    try:
        with open("storage.json", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "storage.json n'existe pas encore."

# On démarre le bot dans un thread séparé
def run_bot():
    bot.start_bot()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)

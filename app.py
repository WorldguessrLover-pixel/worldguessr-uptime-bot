from flask import Flask, jsonify
from storage import load_data
import threading
import bot  # ton script qui gère le bot Telegram

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

@app.route("/show-logs")
def show_logs():
    data = load_data()
    return jsonify(data)

def run_bot():
    bot.run()  # ta fonction principale dans bot.py

if __name__ == "__main__":
    # Lance le bot dans un thread séparé
    t = threading.Thread(target=run_bot)
    t.start()
    
    # Lance le serveur Flask
    app.run(host="0.0.0.0", port=10000)

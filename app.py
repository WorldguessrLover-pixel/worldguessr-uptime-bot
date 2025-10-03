from flask import Flask
import threading
import bot  # <-- on lance ton bot en parallèle

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! 🚀"

# Route pour afficher les logs du storage.json
@app.route('/show-logs')
def show_logs():
    try:
        with open("storage.json", "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "storage.json n'existe pas encore."

def run_bot():
    bot.main()  # ta fonction principale dans bot.py

if __name__ == '__main__':
    # Lancer ton bot dans un thread séparé
    threading.Thread(target=run_bot).start()
    # Démarrer le serveur web (pour Render)
    app.run(host='0.0.0.0', port=10000)

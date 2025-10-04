from flask import Flask
import threading
import time
import bot  # on importe ton fichier bot.py

app = Flask(__name__)

# Route pour vérifier que le service est vivant
@app.route("/")
def home():
    return "OK", 200


# Fonction qui lance la boucle de check
def background_task():
    while True:
        try:
            print("🔄 Lancement du check du leaderboard...")
            bot.run_check()  # appelle la fonction principale de ton bot
        except Exception as e:
            print(f"❌ Erreur dans run_check : {e}")
        time.sleep(300)  # attend 5 minutes (300 secondes)


# Lancer la boucle en parallèle du serveur Flask
def start_background():
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_background()
    app.run(host="0.0.0.0", port=10000)  # Render attend que tu écoutes sur 0.0.0.0

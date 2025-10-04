from flask import Flask, jsonify
import threading
import time
import bot  # on importe ton fichier bot.py

app = Flask(__name__)

# Route simple pour vérifier que le service est vivant
@app.route("/")
def home():
    return "✅ Bot actif", 200


# ➕ (facultatif mais pratique) : route manuelle pour déclencher un check immédiat
@app.route("/force-check")
def force_check():
    try:
        bot.check_leaderboard()
        return jsonify({"status": "ok", "message": "Check lancé manuellement"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def background_task():
    """Boucle de fond qui lance un check toutes les 5 minutes."""
    while True:
        try:
            print("🔄 Lancement du check du leaderboard...")
            bot.check_leaderboard()  # ✅ correction ici !
        except Exception as e:
            print(f"❌ Erreur dans check_leaderboard : {e}")
        time.sleep(300)  # 5 minutes


def start_background():
    """Lance la tâche en arrière-plan au démarrage."""
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_background()
    app.run(host="0.0.0.0", port=10000)

import requests
import os
import time
from datetime import datetime
from storage import load_data, save_data

# Variables d’environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")

CHECK_INTERVAL = 300  # 5 minutes


def fetch_leaderboard():
    """Récupère les données du leaderboard depuis l'URL."""
    try:
        print(f"[{datetime.now()}] 🌐 Requête vers {LEADERBOARD_URL}")
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"[{datetime.now()}] ✅ Données récupérées ({len(data)} entrées)")
        return data
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur lors du fetch leaderboard: {e}")
        return []


def send_telegram_message(message):
    """Envoie un message via Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID non défini")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now()}] 📩 Message envoyé : {message}")
        else:
            print(f"[{datetime.now()}] ⚠️ Erreur envoi Telegram ({response.status_code}) : {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur envoi Telegram: {e}")


def check_leaderboard():
    """Compare le leaderboard actuel avec les données sauvegardées."""
    print(f"[{datetime.now()}] 🔍 Vérification du leaderboard...")

    old_data = load_data()
    old_players = {p["username"]: p["elo"] for p in old_data.get("players", [])}

    new_data = fetch_leaderboard()
    if not new_data:
        print(f"[{datetime.now()}] ⚠️ Aucune donnée reçue, on réessaiera plus tard.")
        return

    messages = []
    new_players = []

    for player in new_data:
        username = player.get("username")
        elo = player.get("elo")

        if not username or elo is None:
            continue

        new_players.append({"username": username, "elo": elo})

        old_elo = old_players.get(username)
        if old_elo is not None and elo != old_elo:
            messages.append(f"⚡ {username} : ELO changé {old_elo} → {elo}")

    save_data(new_players)

    if messages:
        print(f"[{datetime.now()}] 🚀 Changements détectés, envoi Telegram...")
        for msg in messages:
            send_telegram_message(msg)
    else:
        print(f"[{datetime.now()}] ✅ Aucun changement détecté.")


def main():
    """Boucle principale"""
    print("✅ Bot démarré et tourne en continu...")
    while True:
        check_leaderboard()
        time.sleep(CHECK_INTERVAL)

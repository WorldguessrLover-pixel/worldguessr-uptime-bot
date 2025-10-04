import requests
import time
from telegram import Bot
from storage import load_data, save_data

# ⚠️ Mets tes vrais identifiants ici
TELEGRAM_TOKEN = "TON_TELEGRAM_BOT_TOKEN"
CHAT_ID = "TON_CHAT_ID"
LEADERBOARD_URL = "https://worldguessr-leaderboard-url/api"  # à adapter

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message):
    """Envoie un message Telegram via python-telegram-bot"""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"[Telegram] {message}")  # log aussi dans Render
    except Exception as e:
        print(f"Erreur Telegram: {e}")

def fetch_leaderboard():
    """Récupère les données du leaderboard"""
    try:
        response = requests.get(LEADERBOARD_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur fetch leaderboard: {e}")
        return []

def check_updates():
    """Compare leaderboard actuel avec stockage"""
    old_data = load_data()
    old_users = {u["username"]: u["elo"] for u in old_data.get("users", [])}
    
    leaderboard = fetch_leaderboard()
    if not leaderboard:
        print("⚠️ Leaderboard vide ou erreur API")
        return

    updated_users = []
    for entry in leaderboard:
        username = entry.get("username")
        elo = entry.get("elo")
        if not username or elo is None:
            continue

        old_elo = old_users.get(username)
        if old_elo is None:
            send_telegram_message(f"🎉 Nouveau joueur détecté: {username} avec {elo} elo")
        elif elo != old_elo:
            diff = elo - old_elo
            emoji = "⬆️" if diff > 0 else "⬇️"
            send_telegram_message(f"{emoji} {username} est passé de {old_elo} → {elo} elo ({'+' if diff>0 else ''}{diff})")

        updated_users.append({"username": username, "elo": elo})

    save_data(updated_users)
    print(f"[OK] Sauvegarde effectuée avec {len(updated_users)} joueurs")

if __name__ == "__main__":
    while True:
        print("🔄 Vérification du leaderboard...")
        check_updates()
        time.sleep(300)  # 5 minutes

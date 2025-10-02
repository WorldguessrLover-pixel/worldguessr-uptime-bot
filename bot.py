import os
from dotenv import load_dotenv
from leaderboard import fetch_leaderboard
from storage import load_data, save_data
from notifier import send_message

# Charger les variables depuis .env (utile en local)
load_dotenv()

def main():
    # Charger ancien classement
    old_data = load_data()
    # Récupérer nouveau classement
    new_data = fetch_leaderboard()

    changes = []
    for player in new_data.get("players", []):
        name = player["name"]
        elo = player["elo"]

        old_elo = old_data.get(name, {}).get("elo")
        if old_elo and elo != old_elo:
            diff = elo - old_elo
            sign = "🔺" if diff > 0 else "🔻"
            changes.append(f"{name}: {old_elo} → {elo} ({sign}{diff})")

    if changes:
        message = "📊 Mise à jour du leaderboard :\n" + "\n".join(changes)
        send_message(message)

    # Sauvegarder les nouvelles données
    save_data({p["name"]: {"elo": p["elo"]} for p in new_data.get("players", [])})

if __name__ == "__main__":
    main()

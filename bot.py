from storage import load_data, save_data
import requests

def check_leaderboard():
    url = "https://ton-leaderboard-url.com"  # à remplacer
    response = requests.get(url)
    new_data = response.json()

    # Charger l’ancien état
    old_data = load_data()

    # Vérifier les changements (à adapter à ta logique)
    if new_data != old_data:
        # Ici tu envoies ton message Telegram si nécessaire
        print("Changement détecté ✅")

    # Quoi qu’il arrive, on sauvegarde l’état actuel
    save_data(new_data)

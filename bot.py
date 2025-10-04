import os
import requests
from datetime import datetime

LEADERBOARD_URL = os.getenv("LEADERBOARD_URL", "https://api.worldguessr.com/api/leaderboard")

def check_leaderboard():
    print("🔍 Vérification du leaderboard...")
    try:
        print(f"🌐 Requête vers {LEADERBOARD_URL}")
        response = requests.get(LEADERBOARD_URL, timeout=10)

        # Si le code HTTP n’est pas 200
        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code} : {response.text[:200]}")
            return

        # Si le contenu est vide
        if not response.text.strip():
            print("⚠️ Réponse vide reçue de l’API.")
            return

        # Essai de conversion en JSON
        try:
            data = response.json()
        except Exception as e:
            print(f"⚠️ Impossible de décoder la réponse JSON : {e}")
            print(f"🧾 Contenu reçu : {response.text[:500]}")
            return

        # Si l’API a bien renvoyé des données
        print(f"✅ Données récupérées : {len(data)} éléments reçus.")
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Dernière vérification réussie à {now}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête : {e}")

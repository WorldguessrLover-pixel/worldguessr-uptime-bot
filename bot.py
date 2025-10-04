import os
import requests
from datetime import datetime

LEADERBOARD_URL = os.getenv("LEADERBOARD_URL", "https://api.worldguessr.com/api/leaderboard")

def check_leaderboard():
    print("🔍 Vérification du leaderboard...")

    params = {
        "username": "testuser",
        "pastDay": "today",
        "mode": "elo"
    }

    try:
        print(f"🌐 Requête vers {LEADERBOARD_URL} avec paramètres {params}")
        response = requests.get(LEADERBOARD_URL, params=params, timeout=10)

        print(f"📡 Code HTTP : {response.status_code}")

        # Si code ≠ 200
        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"🧾 Contenu : {response.text[:300]}")
            return

        # Si la réponse est vide
        if not response.text.strip():
            print("⚠️ Réponse vide reçue.")
            return

        # Tentative de décodage JSON
        try:
            data = response.json()
            print(f"✅ Réponse JSON correcte — {len(data)} éléments trouvés.")
        except Exception:
            print("⚠️ Réponse non JSON, contenu brut :")
            print(response.text[:500])

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Vérification terminée à {now}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")

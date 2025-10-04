import json
from datetime import datetime

DATA_FILE = "leaderboard_data.json"


def load_data():
    """Charge les données sauvegardées du fichier JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_check": None, "players": []}
    except json.JSONDecodeError:
        return {"last_check": None, "players": []}


def save_data(players):
    """Sauvegarde la liste des joueurs avec l’heure du dernier check."""
    data = {"last_check": datetime.utcnow().isoformat(), "players": players}
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du fichier JSON : {e}")

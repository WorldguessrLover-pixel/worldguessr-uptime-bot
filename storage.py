import json
import os
from datetime import datetime

STORAGE_FILE = "storage.json"

def load_data():
    """Charge le contenu du fichier storage.json"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"last_check": None, "players": []}
    return {"last_check": None, "players": []}

def save_data(players):
    """Sauvegarde les joueurs avec un timestamp dans storage.json"""
    data = {
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "players": players
    }
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

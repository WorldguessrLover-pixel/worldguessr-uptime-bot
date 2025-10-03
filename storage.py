import json
import os

STORAGE_FILE = "storage.json"


def load_data():
    """Charge les anciens ELO depuis storage.json"""
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    """Sauvegarde les ELO actuels dans storage.json"""
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

import json
import os

DATA_FILE = "data.json"

def load_data():
    """Charge les données depuis data.json"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    """Sauvegarde les données dans data.json"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

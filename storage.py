import json
import os

FILE_PATH = "storage.json"

def init_storage():
    """Crée le fichier storage.json s'il n'existe pas encore."""
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f, indent=4)

def load_data():
    """Charge les données depuis storage.json, ou renvoie {} si vide."""
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    """Sauvegarde systématiquement les données dans storage.json."""
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

# On initialise le storage au démarrage
init_storage()

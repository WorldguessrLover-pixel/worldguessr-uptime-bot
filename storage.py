import json
import os

STORAGE_FILE = "data.json"

def load_previous_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

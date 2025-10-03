import json
import os

FILENAME = "leaderboard.json"

def load_previous_data():
    """Charge les données sauvegardées du leaderboard."""
    if not os.path.exists(FILENAME):
        print("[INFO] Aucun fichier précédent trouvé → première exécution.")
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[INFO] Données précédentes chargées ({len(data)} joueurs).")
            return data
    except json.JSONDecodeError:
        print("[WARN] Fichier JSON corrompu → réinitialisation.")
        return []

def save_current_data(data):
    """Sauvegarde les données actuelles du leaderboard."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Données sauvegardées ({len(data)} joueurs).")
    except Exception as e:
        print(f"[ERREUR] Impossible de sauvegarder les données : {e}")

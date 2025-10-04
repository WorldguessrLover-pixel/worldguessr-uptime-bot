# bot.py
import os
import json
import requests
from datetime import datetime
from storage import load_data, save_data

# Variables d'environnement (définies sur Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")

# Seuil d'alerte minimal demandé auparavant (on n'envoie la notif que si new_elo >= THRESHOLD)
ALERT_THRESHOLD = 8000
# Emoji spécial si > 10000
HIGH_ALERT_THRESHOLD = 10000


def fetch_leaderboard():
    """
    Récupère le JSON depuis LEADERBOARD_URL et retourne une liste d'entrées joueurs.
    Cette fonction est robuste : si l'API renvoie {"leaderboard": [...] } ou {"players": [...]}
    elle extrait la liste. Retourne [] en cas d'erreur.
    """
    if not LEADERBOARD_URL:
        print(f"[{datetime.now()}] ❌ LEADERBOARD_URL non défini (variable d'environnement manquante).")
        return []

    try:
        r = requests.get(LEADERBOARD_URL, timeout=12)
        r.raise_for_status()
        data = r.json()

        # DEBUG: afficher le type / clés du JSON retourné (utile pour diagnostiquer)
        if isinstance(data, dict):
            keys = list(data.keys())
            print(f"[{datetime.now()}] 🔍 DEBUG JSON (dict) keys: {keys}")
        else:
            print(f"[{datetime.now()}] 🔍 DEBUG JSON type: {type(data).__name__}")

        # Tentative d'extraction de la liste de joueurs
        if isinstance(data, list):
            players_list = data
        elif isinstance(data, dict):
            for candidate in ("leaderboard", "players", "data", "results", "leaderBoard"):
                if candidate in data and isinstance(data[candidate], list):
                    players_list = data[candidate]
                    break
            else:
                # Si aucune clé connue, chercher la première valeur qui est une liste d'objets plausibles
                players_list = []
                for v in data.values():
                    if isinstance(v, list):
                        players_list = v
                        break
        else:
            players_list = []

        # DEBUG: afficher un aperçu (max 5 éléments) pour confirmer format
        try:
            preview = players_list[:5]
            print(f"[{datetime.now()}] 🔎 Aperçu leaderboard ({len(players_list)} entrées) : {json.dumps(preview, ensure_ascii=False)}")
        except Exception:
            print(f"[{datetime.now()}] 🔎 Aperçu leaderboard: (impossible d'afficher)")

        return players_list if isinstance(players_list, list) else []

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur fetch_leaderboard: {e}")
        return []


def send_telegram_message(text: str):
    """Envoie un message Telegram via l'API simple (requests)."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[{datetime.now()}] ⚠️ Telegram non configuré (TOKEN/CHAT_ID manquants).")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        try:
            result = resp.json()
        except Exception:
            result = resp.text
        print(f"[{datetime.now()}] 📨 Telegram → statut {resp.status_code}, réponse: {result}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur envoi Telegram: {e}")


def check_leaderboard():
    """
    Fonction publique appelée par app.py en arrière-plan.
    - récupère le leaderboard (champ username + elo attendu)
    - compare avec storage.json (champ players)
    - sauvegarde toujours la nouvelle liste via save_data([...])
    - n'envoie des notifs que si un joueur change d'elo ET son nouvel elo >= ALERT_THRESHOLD
      ajoute ⚠️ devant le message si elo >= HIGH_ALERT_THRESHOLD
    """
    print(f"[{datetime.now()}] 🔄 check_leaderboard démarré")

    # Charger données précédentes
    old = load_data()
    old_players_map = {p["username"]: p["elo"] for p in old.get("players", []) if isinstance(p, dict)}

    # Récupérer le leaderboard
    entries = fetch_leaderboard()
    if not entries:
        # Même en cas d'erreur, on met à jour le fichier pour marquer le dernier check (sauvegarde vide)
        save_data([])
        print(f"[{datetime.now()}] ⚠️ Pas d'entrées récupérées, storage mis à jour vide.")
        return

    # Construire nouvelle liste normalisée
    normalized = []
    alerts = []

    for e in entries:
        if not isinstance(e, dict):
            continue
        username = e.get("username") or e.get("user") or e.get("name")
        elo = e.get("elo") if ("elo" in e) else (e.get("rating") if "rating" in e else None)
        # Some APIs might return strings: try cast
        try:
            if isinstance(elo, str) and elo.isdigit():
                elo = int(elo)
        except Exception:
            pass

        if not username or elo is None:
            continue

        normalized.append({"username": username, "elo": elo})

        # Compare vs old
        old_elo = old_players_map.get(username)
        if old_elo is not None and elo != old_elo:
            # Send only if new elo >= threshold
            if elo >= ALERT_THRESHOLD:
                prefix = "⚠️ " if elo >= HIGH_ALERT_THRESHOLD else ""
                diff = elo - old_elo
                sign = "+" if diff > 0 else ""
                alerts.append(f"{prefix}{username} a changé d'ELO : {old_elo} → {elo} ({sign}{diff})")
            else:
                # debug-only: log that change detected but under threshold
                print(f"[{datetime.now()}] ℹ️ Changement détecté pour {username} ({old_elo} → {elo}) mais sous seuil {ALERT_THRESHOLD} → pas de notif")

    # Sauvegarde (toujours)
    save_data(normalized)
    print(f"[{datetime.now()}] ✅ storage.json mis à jour ({len(normalized)} joueurs)")

    # Envoi des notifications (si besoin)
    for msg in alerts:
        send_telegram_message(msg)


# Si on lance bot.py directement pour debug local
if __name__ == "__main__":
    print("Exécution directe de bot.py — lancement d'un check unique (pas de boucle).")
    check_leaderboard()

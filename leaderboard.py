import os
import requests

LEADERBOARD_URL = os.getenv("LEADERBOARD_URL")

def fetch_leaderboard():
    if not LEADERBOARD_URL:
        raise ValueError("LEADERBOARD_URL is not set in environment variables.")
    response = requests.get(LEADERBOARD_URL, timeout=10)
    response.raise_for_status()
    return response.json()

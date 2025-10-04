import os
import json
from flask import Flask

app = Flask(__name__)
STORAGE_FILE = "storage.json"

@app.route("/")
def home():
    return "✅ Bot et API en ligne."

@app.route("/show-logs")
def show_logs():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return app.response_class(
                response=json.dumps(data, indent=4, ensure_ascii=False),
                mimetype="application/json"
            )
        except json.JSONDecodeError:
            return "Erreur: storage.json est corrompu.", 500
    else:
        return "storage.json n'existe pas encore."

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

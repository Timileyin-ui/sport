import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# Simple hardcoded data for demonstration (Replace with real API later)
SPORTS_DATA = {
    "today": "⚽ Football: Arsenal vs Chelsea (20:00)\n🏀 NBA: Lakers vs Warriors (03:30)",
    "score": "⚽ Live: Arsenal 1 - 0 Chelsea (65')\n🏀 Final: Lakers 112 - 108 Warriors"
}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"].lower()

        if "/today" in text:
            send_message(chat_id, SPORTS_DATA["today"])
        elif "/score" in text:
            send_message(chat_id, SPORTS_DATA["score"])
        elif "/start" in text:
            send_message(chat_id, "Welcome! Use /today for fixtures or /score for live results.")
    
    return jsonify({"status": "ok"})

@app.route("/")
def health():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

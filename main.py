import os
import json
from fastapi import FastAPI, Request
import requests

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"
ADMIN_ID = os.getenv("ADMIN_ID")

USERS_FILE = "paid_users.json"

def load_paid_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_paid_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return {"ok": True}

    users = load_paid_users()

    if text.lower() == "/start":
        reply = "👋 Sveiki! Norėdami matyti signalus, naudokite komandą /pay ir atlikite apmokėjimą."
    elif text.lower() == "/pay":
        reply = (
            "📖 Apmokėjimo informacija:\n\n"
            "🏦 Revolut IBAN: LT093250023819440672\n"
            "👛 Trust Wallet adresas: 0xE426ECBa32B0281Ebe0c799512F45E2071a69415\n\n"
            "🧾 Po apmokėjimo parašykite /patvirtinti <user_id> (tik adminui)"
        )
    elif text.lower() == "/signalai":
        if chat_id in users:
            reply = "📊 Signalai:\nBTC/USDT: LONG\nETH/USDT: SHORT"
        else:
            reply = "⛔ Prieiga tik apmokėjusiems. Naudokite /pay."
    elif text.lower().startswith("/patvirtinti"):
        if str(chat_id) != ADMIN_ID:
            reply = "⛔ Tik administratorius gali patvirtinti."
        else:
            parts = text.split()
            if len(parts) == 2:
                try:
                    user_to_add = int(parts[1])
                    if user_to_add not in users:
                        users.append(user_to_add)
                        save_paid_users(users)
                        reply = f"✅ Vartotojas {user_to_add} patvirtintas."
                    else:
                        reply = "👤 Vartotojas jau patvirtintas."
                except:
                    reply = "⚠️ Neteisingas ID formatas."
            else:
                reply = "⚠️ Naudok: /patvirtinti <user_id>"
    else:
        reply = "❓ Nežinoma komanda – naudok /start"

    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "Botas veikia!"}


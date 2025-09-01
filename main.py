import os
import json
from fastapi import FastAPI, Request
import requests

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # pvz.: "123456789"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

USERS_FILE = "paid_users.json"

# ---------- utils ----------
def load_paid_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # leidžiam ir { "users": [...] } ir tiesiog [ ... ]
            if isinstance(data, dict) and "users" in data:
                return list(set(int(x) for x in data["users"]))
            return list(set(int(x) for x in data))
    except Exception:
        return []

def save_paid_users(users):
    users = list({int(x) for x in users})
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def send_message(chat_id: int, text: str, parse_mode: str | None = None):
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        requests.post(f"{API_URL}/sendMessage", json=payload, timeout=10)
    except Exception:
        pass

def is_admin(chat_id: int) -> bool:
    return ADMIN_ID is not None and str(chat_id) == str(ADMIN_ID)

def is_paid(chat_id: int) -> bool:
    return int(chat_id) in load_paid_users()

# ---------- routes ----------
@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}) or {}
    chat = message.get("chat", {}) or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return {"ok": True}

    low = text.lower()

    # /start
    if low == "/start":
        reply = (
            "👋 Sveiki atvykę į *Crypto SignalsAI*!\n\n"
            "Norėdami gauti signalus:\n"
            "1) Naudokite /pay ir atlikite apmokėjimą\n"
            "2) Parašykite /patvirtinti <jūsų_ID> (adminui)\n"
            "3) Gavę patvirtinimą – naudokite /signalai\n\n"
            "Pagalba: /help"
        )
        send_message(chat_id, reply, parse_mode="Markdown")
        return {"ok": True}

    # /help
    if low == "/help":
        reply = (
            "🤖 *Komandos*\n"
            "• /start – pradėti\n"
            "• /pay – apmokėjimo informacija\n"
            "• /info – kaip veikia botas\n"
            "• /signalai – naujausi signalai (tik apmokėjusiems)\n"
            "• /patvirtinti <vartotojo_ID> – admino patvirtinimas\n"
        )
        send_message(chat_id, reply, parse_mode="Markdown")
        return {"ok": True}

    # /info
    if low == "/info":
        reply = (
            "ℹ️ *Kaip veikia botas*\n"
            "1) Atlik apmokėjimą su /pay\n"
            "2) Parašyk /patvirtinti <tavo_ID> – adminas patvirtins\n"
            "3) Tada naudok /signalai, kad gautum naujausius įrašus\n\n"
            "⚠️ Tai nėra finansinis patarimas. Valdyk riziką."
        )
        send_message(chat_id, reply, parse_mode="Markdown")
        return {"ok": True}

    # /pay
    if low == "/pay":
        reply = (
            "💳 *Apmokėjimo informacija*\n\n"
            "🔸 Revolut IBAN: `LT093250023819440672`\n"
            "🔹 Trust Wallet: `0xE426ECBa32B0281Ebe0c799512F45E2071a69415`\n\n"
            "🧾 Po apmokėjimo parašyk: /patvirtinti <tavo_ID>\n"
            "_(tik adminas gali patvirtinti)_"
        )
        send_message(chat_id, reply, parse_mode="Markdown")
        return {"ok": True}

    # /signalai (tik apmokėjusiems)
    if low == "/signalai":
        if is_paid(chat_id):
            # Čia įdėk savo realių signalų generavimą/paėmimą
            reply = (
                "📈 *Naujausi signalai*\n"
                "• BTC/USDT – Long – TP1 $64,800 – SL $61,900\n"
                "• ETH/USDT – Long – TP1 $3,180 – SL $3,020\n"
                "• SOL/USDT – Short – TP1 $139 – SL $151\n\n"
                "✅ Sėkmės! Valdyk riziką."
            )
            send_message(chat_id, reply, parse_mode="Markdown")
        else:
            send_message(
                chat_id,
                "🔒 Prieiga tik apmokėjusiems. Pirmiausia naudok /pay, tada /patvirtinti <tavo_ID>."
            )
        return {"ok": True}

    # /patvirtinti <id> (tik adminui)
    if low.startswith("/patvirtinti"):
        if not is_admin(chat_id):
            send_message(chat_id, "⛔ Tik administratorius gali patvirtinti vartotojus.")
            return {"ok": True}

        parts = text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            send_message(chat_id, "⚠️ Naudok: /patvirtinti <vartotojo_ID>")
            return {"ok": True}

        user_to_add = int(parts[1])
        users = load_paid_users()
        if user_to_add not in users:
            users.append(user_to_add)
            save_paid_users(users)
            send_message(chat_id, f"✅ Vartotojas {user_to_add} patvirtintas.")
            # pranešimas vartotojui
            try:
                send_message(user_to_add, "✅ Jūsų prieiga aktyvuota! Naudokite /signalai.")
            except Exception:
                pass
        else:
            send_message(chat_id, "👤 Šis vartotojas jau patvirtintas.")
        return {"ok": True}

    # nežinoma komanda
    send_message(chat_id, "❓ Nežinoma komanda. Naudok /help")
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "Botas veikia!"}





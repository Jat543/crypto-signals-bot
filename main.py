from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")
REVOLUT_IBAN = os.getenv("REVOLUT_IBAN", "LT093250023819440672")
TRUST_WALLET = os.getenv("TRUST_WALLET", "0xE426ECBa32B0281Ebe0c799512F45E2071a69415")
RAILWAY_URL = "https://crypto-signals-bot-production.up.railway.app"

API = f"https://api.telegram.org/bot{TOKEN}"

# Auto-set webhook at startup
def set_webhook():
    webhook_url = f"{RAILWAY_URL}/{TOKEN}"
    r = requests.get(f"{API}/setWebhook?url={webhook_url}")
    print("Webhook set response:", r.text)

set_webhook()

def send_message(chat_id, text, parse_mode="Markdown"):
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    })

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}

    update = await request.json()
    message = update.get("message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    if not chat_id:
        return {"ok": True}

    # Commands
    if text == "/start":
        reply = (
            "👋 Sveiki! Botas veikia.\n\n"
            "📌 Komandos:\n"
            "/help – Pagalba\n"
            "/pay – Mokėjimo informacija\n"
            "/signalai – Pavyzdiniai signalai\n"
            "/affiliate – Partnerių nuorodos\n"
            "/support – Kontaktas"
        )
        send_message(chat_id, reply)
        return {"ok": True}

    if text == "/help":
        reply = (
            "ℹ️ *Pagalba*\n\n"
            "💳 /pay – Gauti mokėjimo informaciją\n"
            "📊 /signalai – Pavyzdiniai prekybos signalai\n"
            "🌐 /affiliate – Partnerių nuorodos\n"
            "📩 /support – Kontaktinė informacija"
        )
        send_message(chat_id, reply)
        return {"ok": True}

    if text == "/pay":
        reply = (
            f"💳 *Mokėjimo informacija:*\n"
            f"🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n"
            f"👛 Trust Wallet: `{TRUST_WALLET}`\n\n"
            "_Atlikę mokėjimą, parašykite man patvirtinimui._"
        )
        send_message(chat_id, reply)
        return {"ok": True}

    if text == "/signalai":
        reply = (
            "📊 *Pavyzdiniai signalai:*\n"
            "BTC/USDT – Pirkimas @ 30000 🎯\n"
            "ETH/USDT – Pirkimas @ 2000 🎯"
        )
        send_message(chat_id, reply)
        return {"ok": True}

    if text == "/affiliate":
        reply = (
            "🌐 *Partnerių nuorodos:*\n"
            "🔗 Binance: https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK\n"
            "🔗 Kriptomat: https://app.kriptomat.io/ref/join?referral=ghffvpum"
        )
        send_message(chat_id, reply)
        return {"ok": True}

    if text == "/support":
        reply = "📩 Susisiekite su manimi: @CryptoKestas"
        send_message(chat_id, reply)
        return {"ok": True}

    # Default
    send_message(chat_id, f"Gavau: {text}")
    return {"ok": True}


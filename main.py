from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

# Environment variables (nustatyti Railway → Variables)
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

REVOLUT_IBAN = "LT093250023819440672"
TRUST_WALLET = "0xE426ECBa32B0281Ebe0c799512F45E2071a69415"
BINANCE_LINK = "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK"
KRIPTOMAT_LINK = "https://app.kriptomat.io/ref/join?referral=ghffvpum"
SUPPORT_CONTACT = "@CryptoKestas"

# Automatinis webhook nustatymas starto metu
def set_webhook():
    railway_url = "https://crypto-signals-bot-production.up.railway.app"
    webhook_url = f"{railway_url}/{TOKEN}"
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

    if text == "/start":
        send_message(chat_id,
            "👋 Sveiki! Botas veikia.\n\n"
            "📌 Komandos:\n"
            "/help – Pagalba\n"
            "/pay – Mokėjimo informacija\n"
            "/signalai – Pavyzdiniai signalai\n"
            "/affiliate – Partnerių nuorodos\n"
            "/support – Kontaktas"
        )

    elif text == "/help":
        send_message(chat_id,
            "ℹ️ *Pagalba*\n\n"
            "💳 /pay – Mokėjimo informacija\n"
            "📊 /signalai – Pavyzdiniai signalai\n"
            "🌐 /affiliate – Partnerių nuorodos\n"
            "📩 /support – Kontaktas"
        )

    elif text == "/pay":
        send_message(chat_id,
            f"💳 *Mokėjimo informacija:*\n"
            f"🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n"
            f"👛 Trust Wallet: `{TRUST_WALLET}`\n\n"
            "_Atlikę mokėjimą, parašykite man patvirtinimui._"
        )

    elif text == "/signalai":
        send_message(chat_id,
            "📊 *Pavyzdiniai signalai:*\n"
            "BTC/USDT – Pirkimas @ 30000 🎯\n"
            "ETH/USDT – Pirkimas @ 2000 🎯"
        )

    elif text == "/affiliate":
        send_message(chat_id,
            f"🌐 *Partnerių nuorodos:*\n"
            f"🔗 Binance: {BINANCE_LINK}\n"
            f"🔗 Kriptomat: {KRIPTOMAT_LINK}"
        )

    elif text == "/support":
        send_message(chat_id, f"📩 Susisiekite su manimi: {SUPPORT_CONTACT}")

    else:
        send_message(chat_id, f"Gavau: {text}")

    return {"ok": True}



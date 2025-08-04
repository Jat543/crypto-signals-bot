import os
from fastapi import FastAPI, Request
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

REVOLUT_IBAN = os.getenv("REVOLUT_IBAN", "LT093250023819440672")
CRYPTO_ADDRESS = os.getenv("CRYPTO_ADDRESS", "0xE426ECBa32B0281Ebe0c799512F45E2071a69415")
BINANCE_LINK = "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK"
KRIPTOMAT_LINK = "https://app.kriptomat.io/ref/join?referral=ghffvpum"

app = FastAPI()

def send_message(chat_id, text, parse_mode="Markdown"):
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    })

@app.post(f"/{BOT_TOKEN}")
async def telegram_webhook(request: Request):
    data = await request.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").strip()

        if text == "/start":
            send_message(chat_id, "👋 Sveiki! Botas veikia.\n\n📌 Komandos:\n/help – Pagalba\n/pay – Mokėjimo informacija\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")
        
        elif text == "/help":
            send_message(chat_id, "ℹ Pagalba:\nNaudokite šias komandas:\n/pay – Gauti mokėjimo info\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")
        
        elif text == "/pay":
            send_message(chat_id, f"📜 *Mokėjimo informacija:*\n🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n💳 Trust Wallet adresas: `{CRYPTO_ADDRESS}`\n\nAtlikę mokėjimą, parašykite man patvirtinimui.")
        
        elif text == "/signalai":
            send_message(chat_id, "📊 Pavyzdiniai signalai:\n\nBTC/USDT – Pirkimas @ 64000\nETH/USDT – Pirkimas @ 3200\nBNB/USDT – Pirkimas @ 400\n\n⚠ Tai tik pavyzdžiai!")
        
        elif text == "/affiliate":
            send_message(chat_id, f"🤝 Partnerių nuorodos:\n🔗 [Binance registracija]({BINANCE_LINK})\n🔗 [Kriptomat registracija]({KRIPTOMAT_LINK})")
        
        elif text == "/support":
            send_message(chat_id, "📩 Kontaktas: Parašykite čia per Telegram.")

        else:
            send_message(chat_id, f"Gavau: {text}")

    return {"ok": True}

@app.get("/")
def home():
    return {"status": "Bot is running"}




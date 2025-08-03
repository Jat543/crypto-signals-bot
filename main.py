from fastapi import FastAPI, Request
import os, requests

app = FastAPI()

# Bot token iš Railway kintamojo
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

# Mokėjimo duomenys
REVOLUT_IBAN = "LT093250023819440672"
TRUST_WALLET = "0xE426ECBa32B0281Ebe0c799512F45E2071a69415"

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot"}

@app.post(f"/{TOKEN}")
async def telegram_webhook(request: Request):
    update = await request.json()
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id:
        return {"ok": True}

    reply = None

    if text.lower().startswith("/start"):
        reply = "👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu."
    elif text.lower().startswith("/pay"):
        reply = (
            "💳 *Mokėjimo informacija:*\n\n"
            f"🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n"
            f"👛 Trust Wallet: `{TRUST_WALLET}`\n\n"
            "_Atlikę mokėjimą, parašykite mums patvirtinimui._"
        )
    elif text:
        reply = f"Gavau: {text}"
    else:
        reply = "📩 Gauta žinutė."

    # Siunčiam atsakymą į Telegram
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })

    return {"ok": True}







from fastapi import FastAPI, Request
import os, requests

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

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

    if chat_id:
        if text.lower().startswith("/start"):
            reply = "👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu."
        elif text.lower() == "/pay":
            reply = (
    "📜 *Mokėjimo informacija:*\n"
    "🏦 Revolut IBAN: LT093250023819440672\n"
    "👛 Trust Wallet adresas: 0xE426ECBa32B0281Ebe0c799512F45E2071a69415\n\n"
    "_Atlikę mokėjimą, parašykite man patvirtinimui._"
)
            requests.post(f"{API}/sendMessage", json={
                "chat_id": chat_id,
                "text": reply,
                "parse_mode": "Markdown"
            })
            return {"ok": True}
        elif text:
            reply = f"Gavau: {text}"
        else:
            reply = "📩 Gauta žinutė."

        requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": reply})

    return {"ok": True}

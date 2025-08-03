from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

REVOLUT_IBAN = "LT093250023819440672"
TRUST_WALLET = "0xE426ECBa32B0281Ebe0c799512F45E2071a69415"

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    # Leidžia priimti tiek : tiek %3A formą
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}

    update = await request.json()
    message = update.get("message") or update.get("edited_message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    if not chat_id:
        return {"ok": True}

    if text.startswith("/start"):
        reply = "👋 Sveiki! Naudokite /pay, kad pamatytumėte mokėjimo informaciją."
    elif text.startswith("/pay"):
        reply = (
            "💳 *Mokėjimo informacija:*\n\n"
            f"🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n"
            f"👛 Trust Wallet: `{TRUST_WALLET}`\n\n"
            "_Atlikę mokėjimą, parašykite mums patvirtinimui._"
        )
    else:
        reply = f"Gavau: {text}"

    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })

    return {"ok": True}







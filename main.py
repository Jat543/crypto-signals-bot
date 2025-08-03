from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

# Boto tokenas iš Railway kintamojo
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

# Tavo mokėjimo duomenys
REVOLUT_IBAN = "LT093250023819440672"
TRUST_WALLET = "0xE426ECBa32B0281Ebe0c799512F45E2071a69415"

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

# Priimame tiek : tiek %3A
@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}

    update = await request.json()
    message = update.get("message") or update.get("edited_message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    if not chat_id:
        return {"ok": True}

    # Komanda /start
    if text.startswith("/start"):
        reply = (
            "👋 Sveiki! Botas veikia.\n\n"
            "Naudokite komandą /pay, kad pamatytumėte mokėjimo informaciją."
        )

    # Komanda /pay
    elif text.startswith("/pay"):
        reply = (
            "💳 *Mokėjimo informacija:*\n\n"
            f"🏦 Revolut IBAN: `{REVOLUT_IBAN}`\n"
            f"👛 Trust Wallet adresas: `{TRUST_WALLET}`\n\n"
            "_Atlikę mokėjimą, parašykite man patvirtinimui._"
        )

    else:
        reply = f"Gavau: {text}"

    # Siunčiame atsakymą
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })

    return {"ok": True}








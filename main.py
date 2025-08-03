from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

# --- ENV kintamieji ---
TOKEN = os.getenv("BOT_TOKEN")  # tavo boto tokenas iš @BotFather
API = f"https://api.telegram.org/bot{TOKEN}"

# Mokėjimo duomenys (tiesiai čia arba Railway Variables)
REVOLUT_IBAN = os.getenv("REVOLUT_IBAN", "LT093250023819440672")
CRYPTO_ADDRESS = os.getenv("CRYPTO_ADDRESS", "0xE426ECBa32B0281Ebe0c799512F45E2071a69415")

# Pagalbinė funkcija siųsti žinutes
def send(chat_id, text, reply_markup=None, parse_mode=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(f"{API}/sendMessage", json=payload)

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

# Priimame POST į kelią su tokenu (tiek su : tiek su %3A)
@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}

    update = await request.json()

    # Inline mygtukų paspaudimai
    if "callback_query" in update:
        cq = update["callback_query"]
        data = cq.get("data")
        cid = cq["message"]["chat"]["id"]

        if data == "pay_revolut":
            send(cid, f"🏦 Revolut IBAN:\n`{REVOLUT_IBAN}`", parse_mode="Markdown")
        elif data == "pay_crypto":
            send(cid, f"💰 Trust Wallet adresas:\n`{CRYPTO_ADDRESS}`", parse_mode="Markdown")

        requests.post(f"{API}/answerCallbackQuery", json={"callback_query_id": cq["id"]})
        return {"ok": True}

    # Vartotojo žinutės
    message = update.get("message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    if not chat_id:
        return {"ok": True}

    if text == "/start":
        send(chat_id, "👋 Sveiki! Pasirinkite apmokėjimo būdą su /pay")
        return {"ok": True}

    if text == "/pay":
        kb = {
            "inline_keyboard": [
                [{"text": "🏦 Revolut (IBAN)", "callback_data": "pay_revolut"}],
                [{"text": "💰 Trust Wallet", "callback_data": "pay_crypto"}],
            ]
        }
        send(chat_id, "Pasirink apmokėjimo būdą:", reply_markup=kb)
        return {"ok": True}

    if text == "/help":
        send(chat_id, "Pagalba: /start, /pay. Pasirinkite norimą apmokėjimo būdą ir atlikite pavedimą.")
        return {"ok": True}

    send(chat_id, f"Gavau: {text}")
    return {"ok": True}





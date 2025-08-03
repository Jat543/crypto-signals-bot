from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

# --- ENV ---
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")          # Stripe (nebūtina dabar)
REVOLUT_IBAN   = os.getenv("REVOLUT_IBAN")            # LTxx... (naudosim /pay)
CRYPTO_ADDRESS = os.getenv("CRYPTO_ADDRESS")          # 0x... (naudosim /pay)

# --- helperis siuntimui ---
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

# Priimame POST į bet kurį kelią ir normalizuojame tokeną (:%3A)
@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}  # ignoruojam svetimus kelius

    update = await request.json()

    # 0) Inline mygtukų paspaudimai
    if "callback_query" in update:
        cq   = update["callback_query"]
        data = cq.get("data")
        cid  = cq["message"]["chat"]["id"]

        if data == "pay_stripe":
            if PROVIDER_TOKEN:
                send(cid, "Paleidžiu Stripe atsiskaitymą… parašyk /buy")
            else:
                send(cid, "Stripe dar neįjungtas. Galimi: Revolut (IBAN) arba Crypto (Wallet).")
        elif data == "pay_revolut":
            if REVOLUT_IBAN:
                # rodom IBAN; naudok plain text, kad vartotojas nukopijuotų
                send(cid, f"🏦 Revolut IBAN:\n{REVOLUT_IBAN}")
            else:
                send(cid, "Revolut IBAN nenustatytas. Įrašyk REVOLUT_IBAN Railway → Variables.")
        elif data == "pay_crypto":
            if CRYPTO_ADDRESS:
                # suformatuojam taip, kad patogu nukopijuoti
                send(cid, f"💰 Crypto (Trust Wallet) adresas:\n`{CRYPTO_ADDRESS}`", parse_mode="Markdown")
            else:
                send(cid, "Crypto adresas nenustatytas. Įrašyk CRYPTO_ADDRESS Railway → Variables.")

        # privaloma atsakyti, kad dingtu „loading“
        requests.post(f"{API}/answerCallbackQuery", json={"callback_query_id": cq["id"]})
        return {"ok": True}

    # 1) Privaloma: atsakyti į pre_checkout_query (Stripe)
    if "pre_checkout_query" in update:
        pcq = update["pre_checkout_query"]
        requests.post(f"{API}/answerPreCheckoutQuery", json={
            "pre_checkout_query_id": pcq["id"],
            "ok": True
        })
        return {"ok": True}

    # 2) Sėkmingas mokėjimas (Stripe)
    message = update.get("message") or update.get("edited_message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text    = (message.get("text") or "").strip().lower()

    if message.get("successful_payment"):
        sp = message["successful_payment"]
        total = sp.get("total_amount", 0) / 100.0
        currency = (sp.get("currency") or "EUR").upper()
        send(chat_id, f"✅ Apmokėta {total} {currency}. Ačiū!")
        return {"ok": True}

    if not chat_id:
        return {"ok": True}

    # 3) Komandos
    if text == "/start":
        send(
            chat_id,
            "👋 Sveiki! Botas veikia.\n\n"
            "🧾 Apmokėjimai: naudokite /pay (Revolut IBAN / Crypto Wallet / Stripe)."
        )
        return {"ok": True}

    if text == "/pay":
        kb = {
            "inline_keyboard": [
                [{"text": "🏦 Revolut (IBAN)",  "callback_data": "pay_revolut"}],
                [{"text": "💰 Crypto (Wallet)", "callback_data": "pay_crypto"}],
                [{"text": "💳 Stripe (/buy)",   "callback_data": "pay_stripe"}],
            ]
        }
        send(chat_id, "Pasirink apmokėjimo būdą:", reply_markup=kb)
        return {"ok": True}

    if text == "/buy":
        if not PROVIDER_TOKEN:
            send(chat_id, "❗ Stripe neįjungtas. Galite rinktis /pay → Revolut (IBAN) ar Crypto (Wallet).")
            return {"ok": True}

        # Kaina centais (EUR). 990 = 9.90 €
        prices = [{"label": "Crypto Signals – 1 mėn.", "amount": 990}]
        invoice = {
            "chat_id": chat_id,
            "title": "Crypto Signals prenumerata",
            "description": "1 mėn. prieiga prie signalų",
            "payload": "order-001",
            "provider_token": PROVIDER_TOKEN,
            "currency": "EUR",
            "prices": prices,
            "start_parameter": "cs_sub_1m",
            "need_name": True,
            "need_email": True
        }
        requests.post(f"{API}/sendInvoice", json=invoice)
        return {"ok": True}

    if text == "/help":
        send(chat_id, "Pagalba: /start, /pay, /buy. Dėl klausimų – parašykite žinutę.")
        return {"ok": True}

    # 4) Numatytas atsakymas
    send(chat_id, f"Gavau: {text}")
    return {"ok": True}




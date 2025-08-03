from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")  # Stripe provider token iš @BotFather

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

# Priimame POST ir kai kelias turi %3A (naršyklės/Telegram koduoja dvitaškį)
@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}  # ignoruojam neteisingus kelius

    update = await request.json()

    # 1) Privaloma atsakyti į pre_checkout_query (kitaip mokėjimas neužsibaigs)
    if "pre_checkout_query" in update:
        pcq = update["pre_checkout_query"]
        requests.post(f"{API}/answerPreCheckoutQuery", json={
            "pre_checkout_query_id": pcq["id"],
            "ok": True
        })
        return {"ok": True}

    message = update.get("message") or update.get("edited_message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    # 2) Sėkmingo mokėjimo patvirtinimas
    if message.get("successful_payment"):
        sp = message["successful_payment"]
        total = sp.get("total_amount", 0) / 100.0
        currency = (sp.get("currency") or "EUR").upper()
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"✅ Apmokėta {total} {currency}. Ačiū!"
        })
        return {"ok": True}

    if not chat_id:
        return {"ok": True}

    # 3) Komandos
    if text == "/start":
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": "👋 Sveiki! Naudokite /buy norėdami apmokėti testinę sąskaitą."
        })
        return {"ok": True}

    if text == "/buy":
        if not PROVIDER_TOKEN:
            requests.post(f"{API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "❗ Nenurodytas PROVIDER_TOKEN. Įrašyk Railway → Variables ir redeploy."
            })
            return {"ok": True}

        # kaina centais (EUR): 990 = 9.90 €
        prices = [
            {"label": "Crypto Signals – 1 mėn.", "amount": 990}
        ]
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

    # 4) Numatytas atsakymas (echo)
    requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": f"Gavau: {text}"})
    return {"ok": True}


from fastapi import FastAPI, Request
import os, requests, urllib.parse

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

REVOLUT_IBAN = os.getenv("REVOLUT_IBAN", "LT093250023819440672")
TRUST_WALLET = os.getenv("TRUST_WALLET", "0xE426ECBa32B0281Ebe0c799512F45E2071a69415")
BINANCE_LINK = "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK"
KRIPTOMAT_LINK = "https://app.kriptomat.io/ref/join?referral=ghffvpum"

user_lang = {}

def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API}/sendMessage", json=payload)

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot", "expects": f"/{TOKEN}"}

@app.post("/{path}")
async def telegram_webhook(request: Request, path: str):
    normalized = urllib.parse.unquote(path)
    if normalized != TOKEN:
        return {"ok": True}

    update = await request.json()

    # Inline mygtukų pasirinkimai
    if "callback_query" in update:
        cq = update["callback_query"]
        data = cq.get("data")
        cid = cq["message"]["chat"]["id"]

        if data in ["lang_lt", "lang_en"]:
            user_lang[cid] = "lt" if data == "lang_lt" else "en"
            if data == "lang_lt":
                send_message(cid, "✅ Kalba nustatyta į *Lietuvių*. Naudokite /start, /pay, /buy arba /affiliates.")
            else:
                send_message(cid, "✅ Language set to *English*. Use /start, /pay, /buy or /affiliates.")
        elif data == "aff_binance":
            send_message(cid, f"🔗 Binance: {BINANCE_LINK}", parse_mode=None)
        elif data == "aff_kriptomat":
            send_message(cid, f"🔗 Kriptomat: {KRIPTOMAT_LINK}", parse_mode=None)

        requests.post(f"{API}/answerCallbackQuery", json={"callback_query_id": cq["id"]})
        return {"ok": True}

    message = update.get("message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip().lower()

    if not chat_id:
        return {"ok": True}

    lang = user_lang.get(chat_id, None)

    # /start
    if text == "/start":
        kb = {
            "inline_keyboard": [
                [{"text": "🇱🇹 Lietuvių", "callback_data": "lang_lt"},
                 {"text": "🇬🇧 English", "callback_data": "lang_en"}]
            ]
        }
        send_message(chat_id, "🌍 Pasirinkite kalbą / Choose language:", reply_markup=kb)
        return {"ok": True}

    # /pay
    if text == "/pay":
        if lang == "en":
            reply = f"💳 *Payment info:*
🏦 Revolut IBAN: `{REVOLUT_IBAN}`
👛 Trust Wallet: `{TRUST_WALLET}`

_Please confirm after payment._"
        else:
            reply = f"💳 *Mokėjimo informacija:*
🏦 Revolut IBAN: `{REVOLUT_IBAN}`
👛 Trust Wallet: `{TRUST_WALLET}`

_Atlikę mokėjimą, parašykite patvirtinimui._"
        send_message(chat_id, reply)
        return {"ok": True}

    # /buy
    if text == "/buy":
        if lang == "en":
            send_message(chat_id, "💲 Stripe payments will be available soon.")
        else:
            send_message(chat_id, "💲 Stripe mokėjimai bus pridėti netrukus.")
        return {"ok": True}

    # /affiliates
    if text == "/affiliates":
        kb = {
            "inline_keyboard": [
                [{"text": "Binance", "callback_data": "aff_binance"}],
                [{"text": "Kriptomat", "callback_data": "aff_kriptomat"}]
            ]
        }
        if lang == "en":
            send_message(chat_id, "🌐 Choose affiliate link:", reply_markup=kb)
        else:
            send_message(chat_id, "🌐 Pasirinkite partnerio nuorodą:", reply_markup=kb)
        return {"ok": True}

    # Default
    send_message(chat_id, f"Gavau: {text}")
    return {"ok": True}

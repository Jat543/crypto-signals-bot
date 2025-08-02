from fastapi import FastAPI, Request
import os
import httpx

app = FastAPI()

# Token imame iš ENV (Railway → Variables: BOT_TOKEN=...)
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

@app.get("/")
def health():
    return {"ok": True, "service": "CryptoKestasBot"}

# Telegram webhook: POST į /<TOKEN>
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
        elif text:
            reply = f"Gavau: {text}"
        else:
            reply = "📩 Gauta žinutė."

        # Išsiunčiam atsakymą
        async with httpx.AsyncClient() as client:
            await client.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": reply})

    return {"ok": True}

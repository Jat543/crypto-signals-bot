from fastapi import FastAPI, Request
import os

app = FastAPI()
TOKEN = os.getenv("BOT_TOKEN")

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    print("Gauta žinutė:", data)
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "CryptoKestasBot veikia 🚀"}
# main bot logic placeholder

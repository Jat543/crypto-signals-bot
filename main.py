from flask import Flask, request
import telegram

app = Flask(__name__)

# Bot token
TOKEN = "8482491301:AAG5qIUAVUDQDfQpVC-T1jaxQa1w_4ztNeQ"
bot = telegram.Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu.")
    elif text == "/help":
        bot.send_message(chat_id=chat_id, text="""
📌 Komandos:
/pay – Mokėjimo informacija
/signalai – Pavyzdiniai signalai
/affiliate – Partnerių nuorodos
/support – Kontaktas
""")
    elif text == "/pay" or text == "/buy":
        bot.send_message(chat_id=chat_id, text="""
📜 *Mokėjimo informacija:*
🏦 Revolut IBAN: `LT093250023819440672`
👛 Trust Wallet adresas: `0xE426ECBa32B0281Ebe0c799512F45E2071a69415`

_Atlikę mokėjimą, parašykite man patvirtinimui._
""", parse_mode=telegram.ParseMode.MARKDOWN)
    elif text == "/signalai":
        bot.send_message(chat_id=chat_id, text="""
📊 *Pavyzdiniai signalai:*

🟢 BUY BTC/USDT @ 62750
🎯 Target: 64000  
🛑 Stop Loss: 61500  

🟢 BUY ETH/USDT @ 3450  
🎯 Target: 3600  
🛑 Stop Loss: 3350

*Šie signalai yra tik pavyzdžiai.*
""", parse_mode=telegram.ParseMode.MARKDOWN)
    elif text == "/affiliate":
        bot.send_message(chat_id=chat_id, text="""
🔗 *Partnerių nuorodos:*

📈 Binance: [Spausk čia](https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK)  
💱 Kriptomat: [Spausk čia](https://app.kriptomat.io/ref/join?referral=ghffvpum)

_Ačiū, kad naudojiesi mūsų partnerių nuorodomis!_
""", parse_mode=telegram.ParseMode.MARKDOWN)
    elif text == "/support":
        bot.send_message(chat_id=chat_id, text="""
✉️ *Kontaktai:*
Jei turite klausimų – parašykite mums čia Telegram'e arba el. paštu: pagalba@cryptosignalsai.com
""", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=chat_id, text=f"Gavau: {text}")
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)







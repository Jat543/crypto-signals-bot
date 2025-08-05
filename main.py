import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu.")
    elif text == "/help":
        bot.send_message(chat_id=chat_id, text="📌 Komandos:\n/help – Pagalba\n/pay – Mokėjimo informacija\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")
    elif text == "/pay":
        bot.send_message(chat_id=chat_id, text="📜 *Mokėjimo informacija:*\n🏦 Revolut IBAN: LT093250023819440672\n👛 Trust Wallet adresas:\n0xE426ECBa32B0281Ebe0c799512F45E2071a69415\n\n_Atlikę mokėjimą, parašykite man patvirtinimui._", parse_mode=telegram.constants.ParseMode.MARKDOWN)
    elif text == "/signalai":
        bot.send_message(chat_id=chat_id, text="📈 Pavyzdiniai signalai:\n\n🟢 BTC/USDT – LONG @ 27,000\n🎯 Target: 28,500\n🛡️ Stop Loss: 26,400\n\n🟠 ETH/USDT – SHORT @ 1,900\n🎯 Target: 1,750\n🛡️ Stop Loss: 1,980")
    elif text == "/affiliate":
        bot.send_message(chat_id=chat_id, text="🤝 Partnerių nuorodos:\n\n📌 Kriptomat: https://app.kriptomat.io/ref/join?referral=ghffvpum\n📌 Binance: https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK")
    elif text == "/support":
        bot.send_message(chat_id=chat_id, text="📬 Kontaktai:\nEl. paštas: kestas.pociunas@gmail.com\nTelegram: @CryptoKestasBot")
    elif text == "/buy":
        bot.send_message(chat_id=chat_id, text="Norėdami įsigyti prenumeratą, naudokite komandą /pay ir atlikite mokėjimą.")
    else:
        bot.send_message(chat_id=chat_id, text="Komanda neatpažinta. Naudokite /help pagalbai.")

    return 'ok'

@app.route('/')
def index():
    return 'Botas veikia!'

if __name__ == '__main__':
    app.run(debug=True)






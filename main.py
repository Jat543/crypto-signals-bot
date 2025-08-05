import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# Tokenas saugiai iš aplinkos kintamųjų
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN nerastas aplinkos kintamuosiuose.")

# Inicijuojam botą ir Flask
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dispatcher (valdo komandas)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# Komandos
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu.")

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "/start – Pradėti\n"
        "/help – Pagalba\n"
        "/pay – Mokėjimo informacija\n"
        "/buy – Mokėjimo informacija\n"
        "/signalai – Pavyzdiniai signalai\n"
        "/affiliate – Partnerių nuorodos\n"
        "/support – Kontaktas"
    )
    update.message.reply_text(help_text)

def pay(update: Update, context: CallbackContext):
    text = (
        "📜 *Mokėjimo informacija:*\n"
        "🏦 Revolut IBAN: LT093250023819440672\n"
        "👛 Trust Wallet adresas:\n"
        "`0xE426ECBa32B0281Ebe0c799512F45E2071a69415`\n\n"
        "_Atlikę mokėjimą, parašykite man patvirtinimui._"
    )
    update.message.reply_text(text, parse_mode="Markdown")

def signalai(update: Update, context: CallbackContext):
    update.message.reply_text("📈 Pavyzdiniai signalai:\n\nBTC/USDT – Long @ 29,500\nETH/USDT – Short @ 1,850")

def affiliate(update: Update, context: CallbackContext):
    text = (
        "👥 Partnerių nuorodos:\n"
        "🔗 Binance: https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK\n"
        "🔗 Kriptomat: https://app.kriptomat.io/ref/join?referral=ghffvpum"
    )
    update.message.reply_text(text)

def support(update: Update, context: CallbackContext):
    update.message.reply_text("📩 Kontaktai: Parašykite man žinutę čia arba el. paštu kestas.pociunas@gmail.com")

def fallback(update: Update, context: CallbackContext):
    update.message.reply_text("❓ Nežinoma komanda. Naudokite /help kad pamatytumėte galimas komandas.")

# Registruojam komandas
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("pay", pay))
dispatcher.add_handler(CommandHandler("buy", pay))  # alias
dispatcher.add_handler(CommandHandler("signalai", signalai))
dispatcher.add_handler(CommandHandler("affiliate", affiliate))
dispatcher.add_handler(CommandHandler("support", support))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

# Webhook endpointas
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# Paprastas sveikinimas per naršyklę
@app.route('/')
def index():
    return 'Botas veikia!'

# Paleidžiam Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))









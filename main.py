import os
import logging
from flask import Flask, request, abort
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# Aplinkos kintamasis tokenui (nustatyk Railway ar .env faile)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables!")

# Telegram Bot API objektas
bot = telegram.Bot(token=TOKEN)

# Flask aplikacija
app = Flask(__name__)

# Loggerio konfigūracija
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dispatcher su komandų tvarkytojais
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Sveiki! Botas veikia. Parašykite žinutę – atsakysiu."
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/pay – Mokėjimo informacija\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")

def pay(update: Update, context: CallbackContext):
    message = (
        "\U0001F4DC *Mokėjimo informacija:*\n"
        "🏦 Revolut IBAN: LT093250023819440672\n"
        "💼 Trust Wallet adresas:\n"
        "`0xE426ECBa32B0281Ebe0c799512F45E2071a69415`\n\n"
        "_Atlikę mokėjimą, parašykite man patvirtinimui._"
    )
    update.message.reply_markdown(message)

def signalai(update: Update, context: CallbackContext):
    update.message.reply_text("Gavau: /signalai")

def affiliate(update: Update, context: CallbackContext):
    update.message.reply_text("Gavau: /affiliate\n\nBinance: https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK\nKriptomat: https://app.kriptomat.io/ref/join?referral=ghffvpum")

def support(update: Update, context: CallbackContext):
    update.message.reply_text("Gavau: /support\nParašykite mums – atsakysime per 24h.")

def fallback(update: Update, context: CallbackContext):
    update.message.reply_text("Neatpažinau komandos. Naudok /help.")

# Komandų registravimas
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("pay", pay))
dispatcher.add_handler(CommandHandler("signalai", signalai))
dispatcher.add_handler(CommandHandler("affiliate", affiliate))
dispatcher.add_handler(CommandHandler("support", support))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            dispatcher.process_update(update)
        except Exception as e:
            logger.error(f"Klaida apdorojant update: {e}")
        return "ok"
    else:
        abort(403)

@app.route("/")
def index():
    return "Botas veikia!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))








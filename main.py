import os
import stripe
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = os.getenv("STRIPE_DOMAIN", "https://your-domain.com")

bot = Bot(token=TOKEN)
app = Flask(__name__)
stripe.api_key = STRIPE_SECRET_KEY

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Sveiki! Parašykite /buy norėdami įsigyti prieigą prie signalų.")

def buy(update: Update, context: CallbackContext):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Crypto Signalų Prenumerata',
                },
                'unit_amount': 500,  # 5.00 EUR
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/cancel',
    )
    update.message.reply_text(f"Pirkimo nuoroda: {session.url}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("buy", buy))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

@app.route('/')
def index():
    return "Botas veikia!"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
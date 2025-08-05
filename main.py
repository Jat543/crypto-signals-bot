import os
from aiogram import Bot, Dispatcher, executor, types

# Kintamieji iš Railway aplinkos
BOT_TOKEN = os.getenv("BOT_TOKEN")
REVOLUT_IBAN = "LT093250023819440672"
CRYPTO_ADDRESS = "0xE426ECBa32B0281Ebe0c799512F45E2071a69415"
BINANCE_LINK = "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VRLU21DK"
KRIPTOMAT_LINK = "https://app.kriptomat.io/ref/join?referral=ghffvpum"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# /start komanda
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("👋 Sveiki! Botas veikia.\n\n📝 Komandos:\n/help – Pagalba\n/pay – Mokėjimo informacija\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")

# /help komanda
@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.answer("ℹ️ Pagalbos meniu:\n\n/start – Pagrindinis meniu\n/pay – Mokėjimo informacija\n/signalai – Pavyzdiniai signalai\n/affiliate – Partnerių nuorodos\n/support – Kontaktas")

# /pay komanda
@dp.message_handler(commands=["pay"])
async def pay_cmd(message: types.Message):
    text = f"🏦 *Mokėjimo informacija:*\n\n🏛 Revolut IBAN: `{REVOLUT_IBAN}`\n💰 Trust Wallet adresas:\n`{CRYPTO_ADDRESS}`\n\n*Atlikę mokėjimą, parašykite man patvirtinimui.*"
    await message.answer(text, parse_mode="Markdown")

# /signalai komanda
@dp.message_handler(commands=["signalai"])
async def signalai_cmd(message: types.Message):
    await message.answer("📊 Pavyzdiniai signalai:\n\nBTC/USDT – Buy 55000\nETH/USDT – Buy 3200\nBNB/USDT – Buy 600")

# /affiliate komanda
@dp.message_handler(commands=["affiliate"])
async def affiliate_cmd(message: types.Message):
    text = f"🤝 Partnerių nuorodos:\n\n🔹 Binance: {BINANCE_LINK}\n🔹 Kriptomat: {KRIPTOMAT_LINK}"
    await message.answer(text)

# /support komanda
@dp.message_handler(commands=["support"])
async def support_cmd(message: types.Message):
    await message.answer("📩 Pagalba: parašykite čia tiesioginę žinutę arba el. paštu support@cryptosignals.com")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





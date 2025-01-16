import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os

# Tokenni o‘qish
BOT_TOKEN = "8098083094:AAF_0DoWGtJkdDj6EPbHx2kGpmj_g7FgETg"

# Bot va dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# So‘zlar ro‘yxati
with open("words.json", "r") as file:
    words = json.load(file)

# Boshlang‘ich klaviatura
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("New word"))

# /start komandasi
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Inglizcha so‘zlarni o‘rganish uchun 'Yangi so‘z' tugmasini bosing.", 
                        reply_markup=start_keyboard)

# Yangi so‘z komandasi
@dp.message_handler(lambda message: message.text == "Yangi so‘z")
async def send_new_word(message: types.Message):
    word = random.choice(words)
    await message.reply(f"Word: {word['word']}\nTranslation: {word['translation']}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

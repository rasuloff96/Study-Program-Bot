import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os
from dotenv import load_dotenv

# .env fayldan tokenni o‘qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot va dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# So‘zlar ro‘yxatini o‘qish
with open("words.json", "r", encoding="utf-8") as file:
    try:
        words = json.load(file)
        if not words:
            raise ValueError("So‘zlar ro‘yxati bo‘sh!")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Xato: {e}")
        words = []  # Bo‘sh ro‘yxat yoki xato bo‘lsa
        # Kodni to‘xtatish yoki boshqa xatolikni qaytarish

# So'zlarning darajalarini tasniflash (bu masalaning o'ziga mos ravishda kengaytiriladi)
levels = ['Beginner', 'Intermediate', 'Advanced']

# Boshlang‘ich klaviatura
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("Darajani tanlash"))
start_keyboard.add(KeyboardButton("Yangi so‘z"))
start_keyboard.add(KeyboardButton("So‘zlar ro‘yxati"))

# Daraja klaviaturasi
level_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for level in levels:
    level_keyboard.add(KeyboardButton(level))
level_keyboard.add(KeyboardButton("Orqaga"))

# /start komandasi
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Yangi so‘zlarni o‘rganish uchun 'Yangi so‘z' tugmasini bosing.", 
                        reply_markup=start_keyboard)

# Yangi so‘z komandasi
@dp.message_handler(lambda message: message.text == "Yangi so‘z")
async def send_new_word(message: types.Message):
    if words:
        word = random.choice(words)
        await message.reply(f"Word: {word['word']}\nTranslation: {word['translation']}")
    else:
        await message.reply("So‘zlar ro‘yxati bo‘sh. Iltimos, so‘zlarni qo‘shing.")

# So‘zlar ro‘yxatini ko‘rsatish
@dp.message_handler(lambda message: message.text == "So‘zlar ro‘yxati")
async def show_word_list(message: types.Message):
    if words:
        word_list = "\n".join([word['word'] for word in words])
        await message.reply(f"So‘zlar ro‘yxati:\n{word_list}")
    else:
        await message.reply("So‘zlar ro‘yxati bo‘sh. Iltimos, so‘zlarni qo‘shing.")

# Darajani tanlash
@dp.message_handler(lambda message: message.text == "Darajani tanlash")
async def choose_level(message: types.Message):
    await message.reply("Iltimos, o‘rganmoqchi bo‘lgan darajani tanlang.", reply_markup=level_keyboard)

# Foydalanuvchi darajani tanlaganda so'zlar
@dp.message_handler(lambda message: message.text in levels)
async def send_words_by_level(message: types.Message):
    selected_level = message.text
    filtered_words = [word for word in words if word.get('level') == selected_level]
    
    if filtered_words:
        word_list = "\n".join([word['word'] for word in filtered_words])
        await message.reply(f"{selected_level} darajadagi so‘zlar:\n{word_list}")
    else:
        await message.reply(f"{selected_level} darajasi uchun so‘zlar mavjud emas.")

# Orqaga qaytish
@dp.message_handler(lambda message: message.text == "Orqaga")
async def back_to_main_menu(message: types.Message):
    await message.reply("Asosiy menyuga qaytdik.", reply_markup=start_keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

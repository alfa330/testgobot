from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from flask import Flask
import os
import asyncio
import logging

# Initialize Flask app for Render keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "TestGo Bot is running!"

# Initialize aiogram bot
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Welcome message and age verification
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "<b>Добро пожаловать в TestGo! 🚴‍♂️</b>\n"
        "Аренда электровелосипедов для работы и свободы передвижения!\n\n"
        "<b>Вам есть 18 лет?</b>"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Да", callback_data="age_yes"))
    keyboard.add(InlineKeyboardButton("Нет", callback_data="age_no"))
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=keyboard)

# Handle age verification response
@dp.callback_query_handler(lambda c: c.data in ["age_yes", "age_no"])
async def process_age(callback_query: types.CallbackQuery):
    await callback_query.message.delete()  # Remove previous message
    if callback_query.data == "age_no":
        await callback_query.message.answer(
            "<b>Извините! 😔</b>\nАренда доступна только для лиц старше 18 лет.",
            parse_mode="HTML"
        )
    else:
        options_text = (
            "<b>Что вас интересует? 🚴‍♂️</b>\n"
            "Выберите одну из опций ниже:"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Аренда велосипеда", callback_data="rent_bike"))
        keyboard.add(InlineKeyboardButton("Помощь с велосипедом", callback_data="bike_help"))
        await callback_query.message.answer(options_text, parse_mode="HTML", reply_markup=keyboard)

# Handle user selection (rent or help)
@dp.callback_query_handler(lambda c: c.data in ["rent_bike", "bike_help"])
async def process_selection(callback_query: types.CallbackQuery):
    await callback_query.message.delete()  # Remove previous message
    if callback_query.data == "rent_bike":
        rent_text = (
            "<b>Электровелосипед в аренду для курьеров — зарабатывай больше, трать меньше! 🚴‍♂️</b>\n\n"
            "Работаешь в доставке? Хочешь увеличить доход и сократить расходы?\n"
            "<b>Арендуй электровелосипед всего за 20 900 ₸ в неделю</b> и забудь о пробках, транспорте и лишних затратах!\n\n"
            "<b>В комплект входит всё, что нужно для работы без остановок:</b>\n"
            "✅ Надёжный электровелосипед — лёгкий, манёвренный и удобный\n"
            "✅ 2 аккумулятора — до 140 км на одной смене\n"
            "✅ 2 зарядки — заряжай дома за 4 часа\n"
            "✅ Прочный замок — твой байк всегда в безопасности\n\n"
            "<b>Идеально для:</b> Яндекс.Еда, Glovo, Wolt и др.\n"
            "🔥 Без залога\n"
            "🔥 Быстрая выдача\n"
            "🔥 Надёжная техника\n"
            "🔥 Поддержка 24/7\n"
            "🔥 Широкий ассортимент аксессуаров (шлемы, перчатки, защита и т.д.) на пункте выдачи по адресу: <b>Сатпаева 35А (9:00-19:00)</b>\n\n"
            "<b>Выкуп электровелосипеда в Алматы:</b>\n"
            "🚴‍♂️ Забери свой электровелик — работай и выкупай!\n"
            "<b>📍 Где взять?</b> Сатпаева 35А, офис Eazy Go\n"
            "<b>💰 Условия:</b>\n"
            "• Всего 37 500 ₸ в неделю\n"
            "• Выкуп за 5 месяцев — и электровелик твой!\n"
            "• Мощный, с 2 аккумуляторами и полной комплектацией 🔋🔋\n"
            "⚡️ Работай без ограничений в тарифах Курьер и Доставка — зарабатывай больше, пока велосипед окупается сам!\n"
            "<b>📦 Количество ограничено — успей забрать первым!</b>\n"
            "<b>📞 Контакт для аренды:</b> +7 700 808 80 60"
        )
        await callback_query.message.answer(rent_text, parse_mode="HTML")
    else:
        whatsapp_link = "https://wa.me/+77008088060"
        help_text = (
            "<b>Нужна помощь с велосипедом? 🚴‍♂️</b>\n"
            "Свяжитесь с нашей службой поддержки в WhatsApp для быстрого решения любых вопросов!"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Перейти в WhatsApp", url=whatsapp_link))
        await callback_query.message.answer(help_text, parse_mode="HTML", reply_markup=keyboard)

# Run Flask and bot concurrently
if __name__ == '__main__':
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000))))
    flask_thread.start()
    executor.start_polling(dp, skip_updates=True)
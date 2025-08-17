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

# Store user language preference
user_language = {}

# Welcome message and age verification
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "<b>TestGo-ға қош келдіңіз! 🚴‍♂️</b>\n"
        "Жұмысқа және еркін қозғалысқа арналған электровелосипедтерді жалға алу!\n\n"
        "<b>Сізге 18 жас толды ма?</b>\n\n"
        "<b>Добро пожаловать в TestGo! 🚴‍♂️</b>\n"
        "Аренда электровелосипедов для работы и свободы передвижения!\n\n"
        "<b>Вам есть 18 лет?</b>"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("✅", callback_data="age_yes"))
    keyboard.add(InlineKeyboardButton("❌", callback_data="age_no"))
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=keyboard)
    await message.delete() 

# Handle age verification response
@dp.callback_query_handler(lambda c: c.data in ["age_yes", "age_no"])
async def process_age(callback_query: types.CallbackQuery):
    await callback_query.message.delete()  # Remove previous message
    user_id = callback_query.from_user.id
    if callback_query.data == "age_no":
        await callback_query.message.answer(
            "<b>Кешіріңіз! 😔</b>\nЖалға алу тек 18 жастан асқан адамдар үшін қолжетімді.\n\n"
            "<b>Извините! 😔</b>\nАренда доступна только для лиц старше 18 лет.",
            parse_mode="HTML"
        )
    else:
        language_text = (
            "<b>Тілді таңдаңыз / Выберите язык:</b>"
        )
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(InlineKeyboardButton("Қазақша 🇰🇿", callback_data="lang_kz"))
        keyboard.add(InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"))
        user_language[user_id] = None  # Reset language preference
        await callback_query.message.answer(language_text, parse_mode="HTML", reply_markup=keyboard)

# Handle language selection
@dp.callback_query_handler(lambda c: c.data in ["lang_ru", "lang_kz"])
async def process_language(callback_query: types.CallbackQuery):
    await callback_query.message.delete()  # Remove previous message
    user_id = callback_query.from_user.id
    user_language[user_id] = callback_query.data  # Store language preference
    await show_options(callback_query.message, user_id)

# Function to show main options menu
async def show_options(message: types.Message, user_id: int):
    lang = user_language.get(user_id, "lang_ru")
    options_text = (
        "<b>Что вас интересует? 🚴‍♂️</b>\nВыберите одну из опций ниже:"
        if lang == "lang_ru" else
        "<b>Сізді не қызықтырады? 🚴‍♂️</b>\nТөмендегі нұсқалардың бірін таңдаңыз:"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        "Аренда велосипеда 🚲" if lang == "lang_ru" else "Велосипедті жалға алу 🚲",
        callback_data="rent_bike"
    ))
    keyboard.add(InlineKeyboardButton(
        "Помощь с велосипедом 🛠️" if lang == "lang_ru" else "Велосипедпен көмек 🛠️",
        callback_data="bike_help"
    ))
    await message.answer(options_text, parse_mode="HTML", reply_markup=keyboard)

# Function to show rental options menu
async def show_rental_options(message: types.Message, user_id: int):
    lang = user_language.get(user_id, "lang_ru")
    rental_text = (
        "<b>Аренда электровелосипеда 🚴‍♂️</b>\nУзнайте подробности об аренде, что входит в аренду!"
        if lang == "lang_ru" else
        "<b>Электровелосипед жалдау 🚴‍♂️</b>\nЖалдау туралы толық ақпаратпен танысыңыз, жалдауға не кіретінін біліңіз!"
    )
    whatsapp_link = "https://wa.me/+77008088060"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        "Условия аренды 📜" if lang == "lang_ru" else "Жалға алу шарттары 📜",
        callback_data="rent_details"
    ))
    keyboard.add(InlineKeyboardButton(
        "Что входит в комплект 🎒" if lang == "lang_ru" else "Жинақтамаға не кіреді 🎒",
        callback_data="rent_included"
    ))
    keyboard.add(InlineKeyboardButton(
        "Выкуп 💸" if lang == "lang_ru" else "Выкуп 💸",
        callback_data="rent_purchase"
    ))
    keyboard.add(InlineKeyboardButton(
        "Консультация у менеджера 📞" if lang == "lang_ru" else "Менеджерден кеңес алу 📞",
        url=whatsapp_link
    ))
    keyboard.add(InlineKeyboardButton(
        "Назад ⬅️" if lang == "lang_ru" else "Артқа ⬅️",
        callback_data="back_to_options"
    ))
    await message.answer(rental_text, parse_mode="HTML", reply_markup=keyboard)

# Handle user selection (rent, help, back, or rental details)
@dp.callback_query_handler(lambda c: c.data in ["rent_bike", "bike_help", "back_to_options", "rent_details", "rent_included", "rent_purchase"])
async def process_selection(callback_query: types.CallbackQuery):
    await callback_query.message.delete()  # Remove previous message
    user_id = callback_query.from_user.id
    lang = user_language.get(user_id, "lang_ru")
    whatsapp_link = "https://wa.me/+77008088060"
    
    if callback_query.data == "back_to_options":
        await show_options(callback_query.message, user_id)
    elif callback_query.data == "rent_bike":
        await show_rental_options(callback_query.message, user_id)
    elif callback_query.data == "rent_details":
        details_text = (
            "<b>Условия аренды электровелосипеда 🚴‍♂️</b>\n\n"
            "Работаешь в доставке? Хочешь увеличить доход и сократить расходы?\n"
            "<b>Арендуй электровелосипед всего за 20 900 ₸ в неделю</b> и забудь о пробках, транспорте и лишних затратах!\n\n"
            "🔥 Без залога\n"
            "🔥 Быстрая выдача\n"
            "🔥 Надёжная техника\n"
            "<b>Идеально для:</b> Яндекс.Еда, Glovo, Wolt и др.\n"
            "<b>Адрес выдачи:</b> Сатпаева 35А (9:00-19:00)"
            if lang == "lang_ru" else
            "<b>Электровелосипед жалдау шарттары 🚴‍♂️</b>\n\n"
            "Жеткізуде жұмыс істейсіз бе? Табысты арттырып, шығынды азайтқыңыз келе ме?\n"
            "<b>Электровелосипедті аптасына бар болғаны 20 900 ₸-ға жалға алыңыз</b> және кептелістерді, көлікті және артық шығындарды ұмытыңыз!\n\n"
            "🔥 Кепілсіз\n"
            "🔥 Жылдам беру\n"
            "🔥 Сенімді техника\n"
            "<b>Керемет сәйкес келеді:</b> Яндекс.Еда, Glovo, Wolt және т.б.\n"
            "<b>Беру мекенжайы:</b> Сатпаева 35А (9:00-19:00)"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            "Консультация у менеджера 📞" if lang == "lang_ru" else "Менеджерден кеңес алу 📞",
            url=whatsapp_link
        ))
        keyboard.add(InlineKeyboardButton(
            "Назад ⬅️" if lang == "lang_ru" else "Артқа ⬅️",
            callback_data="rent_bike"
        ))
        await callback_query.message.answer(details_text, parse_mode="HTML", reply_markup=keyboard)
    elif callback_query.data == "rent_included":
        included_text = (
            "<b>Что входит в комплект аренды? 🚴‍♂️</b>\n\n"
            "<b>Всё, что нужно для работы без остановок:</b>\n"
            "✅ Надёжный электровелосипед — лёгкий, манёвренный и удобный\n"
            "✅ 2 аккумулятора — до 140 км на одной смене\n"
            "✅ 2 зарядки — заряжай дома за 4 часа\n"
            "✅ Прочный замок — твой байк всегда в безопасности\n"
            "🔥 Широкий ассортимент аксессуаров (шлемы, перчатки, защита и т.д.) на пункте выдачи по адресу: <b>Сатпаева 35А (9:00-19:00)</b>"
            if lang == "lang_ru" else
            "<b>Жалға алу жинақтамасына не кіреді? 🚴‍♂️</b>\n\n"
            "<b>Тоқтаусыз жұмыс істеу үшін барлығы:</b>\n"
            "✅ Сенімді электр велосипед — жеңіл, маневрлі және ыңғайлы\n"
            "✅ 2 аккумулятор — бір ауысымда 140 км-ге дейін\n"
            "✅ 2 зарядтағыш — үйде 4 сағатта зарядтау\n"
            "✅ Мықты құлып — сіздің велосипед әрдайым қауіпсіз\n"
            "🔥 Керек-жарақтардың кең ассортименті (каскалар, қолғаптар, қорғаныс және т.б.) берілетін пунктте: <b>Сәтбаев 35А (9:00-19:00)</b>"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            "Консультация у менеджера 📞" if lang == "lang_ru" else "Менеджерден кеңес алу 📞",
            url=whatsapp_link
        ))
        keyboard.add(InlineKeyboardButton(
            "Назад ⬅️" if lang == "lang_ru" else "Артқа ⬅️",
            callback_data="rent_bike"
        ))
        await callback_query.message.answer(included_text, parse_mode="HTML", reply_markup=keyboard)
    elif callback_query.data == "rent_purchase":
        purchase_text = (
            "<b>Выкуп электровелосипеда в Алматы 🚴‍♂️</b>\n\n"
            "Забери свой электровелик — работай и выкупай!\n"
            "<b>📍 Где взять?</b> Сатпаева 35А, офис Eazy Go\n"
            "<b>💰 Условия:</b>\n"
            "• Всего 37 500 ₸ в неделю\n"
            "• Выкуп за 5 месяцев — и электровелик твой!\n"
            "• Мощный, с 2 аккумуляторами и полной комплектацией 🔋🔋\n"
            "⚡️ Работай без ограничений в тарифах Курьер и Доставка — зарабатывай больше, пока велосипед окупается сам!\n"
            "<b>📦 Количество ограничено — успей забрать первым!</b>\n"
            if lang == "lang_ru" else
            "<b>Алматыда электровелосипедті сатып алу 🚴‍♂️</b>\n\n"
            "Өз электровелиңді ал — жұмыс істеп, сатып ал!\n"
            "<b>📍 Қайдан алуға болады?</b> Сатпаева 35А, Eazy Go офисі\n"
            "<b>💰 Шарттар:</b>\n"
            "• Аптасына бар болғаны 37 500 ₸\n"
            "• 5 айда толық сатып алу — электровелик сенің болады!\n"
            "• Қуатты, 2 аккумулятормен және толық жинақпен 🔋🔋\n"
            "⚡️ Курьер және Жеткізу тарифтерінде шектеусіз жұмыс істе — велосипед өз-өзін өтегенше көбірек тап!\n"
            "<b>📦 Саны шектеулі — алғашқылардың бірі болып үлгер!</b>\n"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            "Консультация у менеджера 📞" if lang == "lang_ru" else "Менеджерден кеңес алу 📞",
            url=whatsapp_link
        ))
        keyboard.add(InlineKeyboardButton(
            "Назад ⬅️" if lang == "lang_ru" else "Артқа ⬅️",
            callback_data="rent_bike"
        ))
        await callback_query.message.answer(purchase_text, parse_mode="HTML", reply_markup=keyboard)
    else:  # bike_help
        help_text = (
            "<b>Нужна помощь с велосипедом? 🚴‍♂️</b>\n"
            "Свяжитесь с нашей службой поддержки в WhatsApp для быстрого решения любых вопросов!"
            if lang == "lang_ru" else
            "<b>Велосипедпен көмек керек пе? 🚴‍♂️</b>\n"
            "Кез келген сұрақты тез шешу үшін біздің қолдау қызметімен WhatsApp арқылы байланысыңыз!"
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            "Перейти в WhatsApp 📞" if lang == "lang_ru" else "WhatsApp-қа өту 📞",
            url=whatsapp_link
        ))
        keyboard.add(InlineKeyboardButton(
            "Назад ⬅️" if lang == "lang_ru" else "Артқа ⬅️",
            callback_data="back_to_options"
        ))
        await callback_query.message.answer(help_text, parse_mode="HTML", reply_markup=keyboard)

# Run Flask and bot concurrently
if __name__ == '__main__':
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000))))
    flask_thread.start()
    executor.start_polling(dp, skip_updates=True)
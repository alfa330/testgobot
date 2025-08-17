from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from flask import Flask
import os
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

# Dictionary for languages
TEXTS = {
    "ru": {
        "welcome": "<b>Добро пожаловать в TestGo! 🚴‍♂️</b>\nАренда электровелосипедов для работы и свободы передвижения!\n\n<b>Вам есть 18 лет?</b>",
        "age_no": "<b>Извините! 😔</b>\nАренда доступна только для лиц старше 18 лет.",
        "choose_lang": "Выберите язык 🇷🇺🇰🇿",
        "menu": "<b>Что вас интересует? 🚴‍♂️</b>\nВыберите одну из опций ниже:",
        "rent": "Аренда велосипеда 🚲",
        "help": "Помощь с велосипедом 🛠️",
        "rent_menu": "<b>Аренда электровелосипеда 🚴‍♂️</b>\nУзнайте подробности об аренде, комплектации или выкупе!",
        "rent_details": "<b>Условия аренды электровелосипеда 🚴‍♂️</b>\n\nРаботаешь в доставке? Хочешь увеличить доход и сократить расходы?\n<b>Арендуй электровелосипед всего за 20 900 ₸ в неделю</b> и забудь о пробках, транспорте и лишних затратах!\n\n🔥 Без залога\n🔥 Быстрая выдача\n🔥 Надёжная техника\n🔥 Поддержка 24/7\n<b>Идеально для:</b> Яндекс.Еда, Glovo, Wolt и др.\n<b>Адрес выдачи:</b> Сатпаева 35А (9:00-19:00)",
        "rent_included": "<b>Что входит в комплект аренды? 🚴‍♂️</b>\n\n<b>Всё, что нужно для работы без остановок:</b>\n✅ Надёжный электровелосипед — лёгкий, манёвренный и удобный\n✅ 2 аккумулятора — до 140 км на одной смене\n✅ 2 зарядки — заряжай дома за 4 часа\n✅ Прочный замок — твой байк всегда в безопасности\n🔥 Широкий ассортимент аксессуаров на пункте выдачи по адресу: <b>Сатпаева 35А (9:00-19:00)</b>",
        "rent_purchase": "<b>Выкуп электровелосипеда в Алматы 🚴‍♂️</b>\n\nЗабери свой электровелик — работай и выкупай!\n<b>📍 Где взять?</b> Сатпаева 35А, офис Eazy Go\n<b>💰 Условия:</b>\n• Всего 37 500 ₸ в неделю\n• Выкуп за 5 месяцев — и электровелик твой!\n• Мощный, с 2 аккумуляторами и полной комплектацией 🔋🔋\n⚡️ Работай без ограничений в тарифах Курьер и Доставка\n<b>📦 Количество ограничено!</b>\n<b>📞 Контакт:</b> +7 700 808 80 60",
        "help_text": "<b>Нужна помощь с велосипедом? 🚴‍♂️</b>\nСвяжитесь с нашей службой поддержки в WhatsApp!",
        "consult": "📞 Консультация у менеджера",
        "back": "⬅️ Назад"
    },
    "kz": {
        "welcome": "<b>TestGo-ға қош келдіңіз! 🚴‍♂️</b>\nЖұмыс пен еркін қозғалыс үшін электровелосипедтерді жалға алу!\n\n<b>Сізге 18 жас толды ма?</b>",
        "age_no": "<b>Кешіріңіз! 😔</b>\nЖалға алу тек 18 жастан асқандарға қолжетімді.",
        "choose_lang": "Тілді таңдаңыз 🇷🇺🇰🇿",
        "menu": "<b>Сізді не қызықтырады? 🚴‍♂️</b>\nТөменнен таңдаңыз:",
        "rent": "Велосипед жалдау 🚲",
        "help": "Велосипедке көмек 🛠️",
        "rent_menu": "<b>Электровелосипед жалдау 🚴‍♂️</b>\nЖалдау, жиынтық немесе сатып алу туралы біліңіз!",
        "rent_details": "<b>Электровелосипедті жалдау шарттары 🚴‍♂️</b>\n\nДоставкада істейсіз бе? Кірісті арттырғыңыз келе ме?\n<b>Электровелосипедті аптасына небәрі 20 900 ₸</b> жалға алыңыз!\n\n🔥 Кепілсіз\n🔥 Жылдам рәсімдеу\n🔥 Сенімді техника\n🔥 24/7 қолдау\n<b>Жарамды:</b> Яндекс.Еда, Glovo, Wolt және т.б.\n<b>Мекен-жай:</b> Сатпаева 35А (9:00-19:00)",
        "rent_included": "<b>Жалдау жиынтығына не кіреді? 🚴‍♂️</b>\n\n<b>Жұмыс үшін бәрі:</b>\n✅ Сенімді электровелосипед\n✅ 2 аккумулятор — бір ауысымға дейін 140 км\n✅ 2 зарядтағыш — үйде 4 сағатта зарядтау\n✅ Берік құлып\n🔥 Қосымша керек-жарақтар (шлем, қолғап, т.б.) — <b>Сатпаева 35А</b>",
        "rent_purchase": "<b>Алматыда электровелосипедті сатып алу 🚴‍♂️</b>\n\nӨз велигіңді ал да, жұмыс істей жүріп төле!\n<b>📍 Мекен-жай:</b> Сатпаева 35А, Eazy Go офисі\n<b>💰 Шарттары:</b>\n• Аптасына 37 500 ₸\n• 5 айда толық төленеді — велосипед сіздікі!\n• Қуатты, 2 аккумулятормен 🔋🔋\n⚡️ Курьер мен Доставка тарифтерінде шектеусіз жұмыс істеңіз!\n<b>📦 Шектеулі!</b>\n<b>📞 Байланыс:</b> +7 700 808 80 60",
        "help_text": "<b>Велосипедке көмек керек пе? 🚴‍♂️</b>\nЖылдам шешім үшін WhatsApp арқылы байланысыңыз!",
        "consult": "📞 Менеджер кеңесі",
        "back": "⬅️ Артқа"
    }
}

# Store user language
user_lang = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Да", callback_data="age_yes"),
        InlineKeyboardButton("❌ Нет", callback_data="age_no")
    )
    await message.answer(TEXTS["ru"]["welcome"], parse_mode="HTML", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["age_yes", "age_no"])
async def process_age(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    if callback_query.data == "age_no":
        await callback_query.message.answer(TEXTS["ru"]["age_no"], parse_mode="HTML")
    else:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz")
        )
        await callback_query.message.answer(TEXTS["ru"]["choose_lang"], parse_mode="HTML", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["lang_ru", "lang_kz"])
async def set_language(callback_query: types.CallbackQuery):
    lang = "ru" if callback_query.data == "lang_ru" else "kz"
    user_lang[callback_query.from_user.id] = lang
    await callback_query.message.delete()
    await show_options(callback_query.message, lang)

async def show_options(message: types.Message, lang="ru"):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🚲 " + TEXTS[lang]["rent"], callback_data="rent_bike"),
        InlineKeyboardButton("🛠️ " + TEXTS[lang]["help"], callback_data="bike_help")
    )
    await message.answer(TEXTS[lang]["menu"], parse_mode="HTML", reply_markup=keyboard)

async def show_rental_options(message: types.Message, lang="ru"):
    whatsapp_link = "https://wa.me/+77008088060"
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📄 Условия" if lang=="ru" else "📄 Шарттар", callback_data="rent_details"),
        InlineKeyboardButton("📦 Комплект" if lang=="ru" else "📦 Жиынтық", callback_data="rent_included"),
        InlineKeyboardButton("💰 Выкуп" if lang=="ru" else "💰 Сатып алу", callback_data="rent_purchase"),
        InlineKeyboardButton(TEXTS[lang]["consult"], url=whatsapp_link),
        InlineKeyboardButton(TEXTS[lang]["back"], callback_data="back_to_options")
    )
    await message.answer(TEXTS[lang]["rent_menu"], parse_mode="HTML", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["rent_bike", "bike_help", "back_to_options", "rent_details", "rent_included", "rent_purchase"])
async def process_selection(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    lang = user_lang.get(callback_query.from_user.id, "ru")
    whatsapp_link = "https://wa.me/+77008088060"

    if callback_query.data == "back_to_options":
        await show_options(callback_query.message, lang)
    elif callback_query.data == "rent_bike":
        await show_rental_options(callback_query.message, lang)
    elif callback_query.data == "rent_details":
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["consult"], url=whatsapp_link))
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["back"], callback_data="rent_bike"))
        await callback_query.message.answer(TEXTS[lang]["rent_details"], parse_mode="HTML", reply_markup=keyboard)
    elif callback_query.data == "rent_included":
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["consult"], url=whatsapp_link))
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["back"], callback_data="rent_bike"))
        await callback_query.message.answer(TEXTS[lang]["rent_included"], parse_mode="HTML", reply_markup=keyboard)
    elif callback_query.data == "rent_purchase":
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["consult"], url=whatsapp_link))
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["back"], callback_data="rent_bike"))
        await callback_query.message.answer(TEXTS[lang]["rent_purchase"], parse_mode="HTML", reply_markup=keyboard)
    else:  # bike_help
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("📲 WhatsApp", url=whatsapp_link))
        keyboard.add(InlineKeyboardButton(TEXTS[lang]["back"], callback_data="back_to_options"))
        await callback_query.message.answer(TEXTS[lang]["help_text"], parse_mode="HTML", reply_markup=keyboard)

if __name__ == '__main__':
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000))))
    flask_thread.start()
    executor.start_polling(dp, skip_updates=True)

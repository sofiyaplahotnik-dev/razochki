import datetime
import telebot
from telebot import types

# Ваш действующий токен
TOKEN = '8892725472:AAFUuGjvGw0JIhqlFZ4l9B-0w-Yh-vFT6DM'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения дат пользователей
user_dates = {}

def get_sleeps_left(target_date):
    """Сколько разочков осталось поспать до мур мур мур"""
    today = datetime.date.today()
    delta = target_date - today
    return max(0, delta.days)

def get_main_keyboard():
    """Создает меню с кнопками."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_check = types.KeyboardButton("Сколько разочков осталось поспать?")
    btn_change = types.KeyboardButton("Установить новую дату")
    markup.add(btn_check, btn_change)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Сколько разчков надо поспать, чтобы наконец-то мур мур мур\n\n"
        "Сначала нажми кнопку 'Установить новую дату' ниже.",
        reply_markup=get_main_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == "Установить новую дату")
def ask_for_date(message):
    msg = bot.send_message(
        message.chat.id, 
        "Дата до мур мур мур ДД.ММ.ГГГГ (например: 31.12.2026):",
        reply_markup=types.ReplyKeyboardRemove() # Временно убираем кнопки, чтобы не мешали вводу
    )
    bot.register_next_step_handler(msg, process_date)

def process_date(message):
    try:
        # Пробуем прочитать дату
        parsed_date = datetime.datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
        user_dates[message.chat.id] = parsed_date
        
        bot.send_message(
            message.chat.id, 
            f"Дата успешно сохранена: {parsed_date.strftime('%d.%m.%Y')}", 
            reply_markup=get_main_keyboard()
        )
    except ValueError:
        # Если формат ввода неверный
        msg = bot.send_message(
            message.chat.id, 
            "Напиши дату цифрами через точки: 31.12.2026\nПопробуйте еще раз:",
        )
        bot.register_next_step_handler(msg, process_date)

@bot.message_handler(func=lambda message: message.text == "Сколько разочков осталось поспать?")
def check_sleeps(message):
    chat_id = message.chat.id
    if chat_id not in user_dates:
        bot.send_message(
            chat_id, 
            "Нажми кнопку 'Установить новую дату'.",
            reply_markup=get_main_keyboard()
        )
        return

    target_date = user_dates[chat_id]
    sleeps = get_sleeps_left(target_date)
    formatted_date = target_date.strftime('%d.%m.%Y')
    
    if sleeps > 0:
        bot.send_message(message.chat.id, f"До мур мур мур ( {formatted_date} ) осталось поспать {sleeps} разочков..")
    else:
        bot.send_message(message.chat.id, f"Дата {formatted_date} уже наступила или прошла!")

if __name__ == '__main__':
    print("Бот успешно перезапущен и готов к работе!")
    bot.infinity_polling()

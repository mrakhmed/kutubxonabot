import telebot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
)
BOT_TOKEN = ""
CHANNEL_ID = ""


bot = telebot.TeleBot(BOT_TOKEN)

data = {}


def get_complaint_data(message):
    text = f"Ism: {data[message.from_user.id]['name']}\n"
    text += f"Telefon: {data[message.from_user.id]['phone_number']}\n\n"
    text += f"Javob: {data[message.from_user.id]['complaint']}"
    return text


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Assalomu aleykum Savol-Javob botiga xush kelibsiz!!!\n\n"
    text += "Iltimos ismingizni kiriting"
    data[message.from_user.id] = {'step': 'ENTER_FIRST_NAME'}
    bot.send_message(message.from_user.id, text)


@bot.message_handler(content_types=['contact'])
def contact_message(message):
    user_step = data[message.from_user.id]['step']
    if user_step == "ENTER_PHONE_NUMBER":
        data[message.from_user.id]['phone_number'] = message.contact.phone_number
        data[message.from_user.id]['step'] = "ENTER_YOUR_COMPLAINT"

        text = "Telefon raqamingiz qabul qilindi\n\n"
        text += "Endi iltimos Javobni yozma tarzda yuboring"

        bot.send_message(message.from_user.id, text)


@bot.message_handler(func=lambda m: True)
def text_message(message):
    user_step = data[message.from_user.id]['step']
    if user_step == "ENTER_FIRST_NAME":
        data[message.from_user.id]['name'] = message.text
        data[message.from_user.id]['step'] = "ENTER_PHONE_NUMBER"

        reply_markup = ReplyKeyboardMarkup(
            row_width=1,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        reply_markup.add(
            KeyboardButton(
                text="Telefon raqamni jonatish",
                request_contact=True
            )
        )
        text = "Iltimos telefon raqamingizni jo'nating\n\n"
        text += 'Quyidagi tarzda: +998XXXXXXXXX'
        bot.send_message(message.from_user.id, text, reply_markup=reply_markup)
    elif user_step == "ENTER_PHONE_NUMBER":
        try:
            phone_number = int(message.text)
            data[message.from_user.id]['phone_number'] = phone_number
            data[message.from_user.id]['step'] = "ENTER_YOUR_COMPLAINT"

            text = "Telefon raqamingiz qabul qilindi\n\n"
            text += "Endi iltimos Javobni yozma tarzda yuboring"
            print(data)
            bot.send_message(message.from_user.id, text)
        except Exception as e:
            bot.send_message(message.from_user.id, "Iltimos telefon raqamingizni togri kiriting!!!")
    elif user_step == "ENTER_YOUR_COMPLAINT":
        data[message.from_user.id]['complaint'] = message.text

        inline_markup = InlineKeyboardMarkup(row_width=2)
        inline_markup.add(*[
            InlineKeyboardButton(text="HA", callback_data="yes"),
            InlineKeyboardButton(text="YO'Q", callback_data="no"),
        ])
        text = get_complaint_data(message)
        bot.send_message(message.from_user.id, text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda c: True)
def callback_message(callback):
    try:
        if callback.data == 'yes':
            bot.delete_message(callback.from_user.id, callback.message.message_id)
            bot.send_message(
                callback.from_user.id,
                "Raxmat arizangiz qabul qilindi !!! Botni qaytadan ishga tushirish uchun /start kommandasini kiriting!!!",
            )
            text = get_complaint_data(callback)
            bot.send_message(CHANNEL_ID, text)
    except Exception as e:
        print(e)

    print(callback.data)


bot.polling(none_stop=True)

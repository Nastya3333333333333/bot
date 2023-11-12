import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import telebot;
from telebot import types


load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(telegram_token)
user_dates = {}
months_list = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень",
               "Жовтень", "Листопад", "Грудень"]
month_texts = [
    "Текст 1", "Текст 2", "Текст 3", "Текст 4", "Текст 5", "Текст 6", "Текст 7", "Текст 8", "Текст 9", "Текст 10",
    "Текст 11", "Текст 12", "Текст 13", "Текст 14", "Текст 15", "Текст 16", "Текст 17", "Текст 18", "Текст 19", "Текст 20", "Текст 21", "Текст 22"
]

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привіт! Будь ласка, введіть вашу дату народження у форматі ДД-ММ-РРРР.")

@bot.callback_query_handler(func=lambda call: call.data == "pay")
def handle_pay(call):
    chat_id = call.message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(months_list), 3):
        row_buttons = [
            types.KeyboardButton(text=month)
            for month in months_list[i:i + 3]
        ]
        keyboard.row(*row_buttons)
    bot.send_message(chat_id, "Можливість оплати з'явиться найближчим часом.")
    bot.send_message(chat_id, "Оберіть місяць:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    inline_markup = None
    if chat_id not in user_dates:
        try:
            parsed_date = parser.parse(message.text, dayfirst=True)
            user_dates[chat_id] = parsed_date.strftime('%d-%m-%Y')
            inline_markup = types.InlineKeyboardMarkup(row_width=3)
            inline_markup.add(types.InlineKeyboardButton(text="Оплатити", callback_data="pay"))
            bot.send_message(chat_id, "Оплатіть, щоб продовжити:", reply_markup=inline_markup)
        except ValueError:
            bot.send_message(chat_id, "Неправильний формат дати. Будь ласка, введіть дату у коректному форматі.")
    else:
        selected_month = message.text
        if selected_month and selected_month in months_list:
            month_index = months_list.index(selected_month)
            date_text = user_dates[chat_id]
            day, month, year = map(int, date_text.split('-'))
            selected_month_index = month_index + 1
            texts_index = (day + month + selected_month_index+8) % 22
            bot.send_message(chat_id, month_texts[texts_index])

        else:
            bot.send_message(chat_id, "Виберіть місяць.")

if __name__ == "__main__":
    bot.polling(none_stop=True)

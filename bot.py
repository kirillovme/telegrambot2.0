import telebot
from telebot import types
from util.moneycurs import *

bot = telebot.TeleBot('1313518366:AAHBOBQXYIY3UYa8IjOvn-r4TPj8oPiwXvI')


@bot.message_handler(commands=['start', 'help'])
def send_commands(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/textorimg', '/currency')
    bot.send_message(message.chat.id, "The bot has started!", reply_markup=start_markup)


@bot.message_handler(commands=['textorimg'])
def img_command(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    sent = bot.send_message(message.chat.id, "Отправьте фото или картинку и бот определит, что вы отправили.",
                            reply_markup=hide_markup)
    bot.register_next_step_handler(sent, get_input)


def get_input(message):
    if message.content_type == 'text':
        sent = bot.send_message(message.chat.id, "Вы ввели текст.")
    if message.content_type == 'photo':
        sent = bot.send_message(message.chat.id, "Вы отправили изображение.")
    bot.register_next_step_handler(sent, send_commands)


@bot.message_handler(commands=['currency'])
def cur_command(message):
    money_markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in currencies.items():
        money_markup.add(types.InlineKeyboardButton(text=key, callback_data=value))
    bot.send_message(message.chat.id, "Choose the money:", reply_markup=money_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_currencies(call):
    if call.message:
        money_switcher = {
            'USD': f"💰Dollar:  {usd_price} руб",
            'EUR': f"💰Euro: {eur_price} руб",
            'CAD': f"💰Canadian Dollar: {cad_price} руб"
        }
    money_response = money_switcher.get(call.data)
    if money_response:
        bot.send_message(call.message.chat.id, money_response)


bot.polling(none_stop=True, interval=0)

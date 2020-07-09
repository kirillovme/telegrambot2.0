import telebot
from telebot import types
from util.moneycurs import *
from datetime import datetime
from util.db_connection import *

bot = telebot.TeleBot('1313518366:AAHBOBQXYIY3UYa8IjOvn-r4TPj8oPiwXvI')

current_money = ""
current_value = 0


def outro_handler(chat_id):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/textorimg', '/currency', '/exchange', '/history')
    bot.send_message(chat_id, "Вы возвращены в главное меню", reply_markup=start_markup)


@bot.message_handler(commands=['start', 'help'])
def send_commands(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/textorimg', '/currency', '/exchange', '/history')
    bot.send_message(message.chat.id, "The bot has started!", reply_markup=start_markup)


@bot.message_handler(commands=['textorimg'])
def img_command(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    sent = bot.send_message(message.chat.id, "Отправьте фото или картинку и бот определит, что вы отправили.",
                            reply_markup=hide_markup)
    bot.register_next_step_handler(sent, get_input)


def get_input(message):
    if message.content_type == 'text':
        bot.send_message(message.chat.id, "Вы ввели текст.")
    elif message.content_type == 'photo':
        bot.send_message(message.chat.id, "Вы отправили изображение.")
    else:
        bot.send_message(message.chat.id, "Вы отправили что-то другое.")
    outro_handler(message.chat.id)


@bot.message_handler(commands=['currency'])
def cur_command(message):
    money_markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in currencies.items():
        money_markup.add(types.InlineKeyboardButton(text=key, callback_data=value))
    bot.send_message(message.chat.id, "Choose the money:", reply_markup=money_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_currencies(call):
    if call.message:
        global current_money
        if call.data == "USD" or call.data == "EUR" or call.data == "CAD":
            money_switcher = {
                'USD': f"💰Dollar:  {usd_price} руб",
                'EUR': f"💰Euro: {eur_price} руб",
                'CAD': f"💰Canadian Dollar: {cad_price} руб"
            }
            money_response = money_switcher.get(call.data)
            if money_response:
                bot.send_message(call.message.chat.id, money_response)
        if call.data == "dollar":
            bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
            current_money = "dollar"
            sent = bot.send_message(call.message.chat.id,
                                    "Введите количество рублей для перевода, если значение не целое,"
                                    "то вводите через точку.")
            bot.register_next_step_handler(sent, input_value)
        elif call.data == "euro":
            bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
            current_money = "euro"
            sent = bot.send_message(call.message.chat.id,
                                    "Введите количество рублей для перевода, если значение не целое,"
                                    "то вводите через точку.")
            bot.register_next_step_handler(sent, input_value)
        elif call.data == "cdollar":
            bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup='')
            current_money = "cdollar"
            sent = bot.send_message(call.message.chat.id,
                                    "Введите количество рублей для перевода, если значение не целое,"
                                    "то вводите через точку.")
            bot.register_next_step_handler(sent, input_value)


@bot.message_handler(commands=['exchange'])
def ex_command(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    money_markup = types.InlineKeyboardMarkup(row_width=1)
    money_markup.add(types.InlineKeyboardButton(text="USA Dollar", callback_data="dollar"))
    money_markup.add(types.InlineKeyboardButton(text="Euro", callback_data="euro"))
    money_markup.add(types.InlineKeyboardButton(text="Canadian dollar", callback_data="cdollar"))
    bot.send_message(message.chat.id, "Клавиатура скрыта", reply_markup=hide_markup)
    bot.send_message(message.chat.id, "Choose the valute:", reply_markup=money_markup)


def input_value(message):
    global current_value
    try:
        current_value = float(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Через точку!")
        current_value = None
    global current_money
    cur = conn.cursor()
    if current_value is None:
        bot.send_message(message.chat.id, "Всё неправильно ввёл, давай заново.")
    elif current_money == "dollar":
        exchange_result = current_value / usd_price
        bot.send_message(message.chat.id, exchange_result)
        try:
            record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                                message.chat.id, datetime.fromtimestamp(message.date))
            cur.execute(postgre_insert_query, record_to_insert)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            if conn:
                bot.send_message(message.chat.id, "Failed to insert try again")
        finally:
            if conn:
                cur.close()
    elif current_money == "euro":
        exchange_result = current_value / eur_price
        bot.send_message(message.chat.id, exchange_result)
        try:
            record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                                message.chat.id, datetime.fromtimestamp(message.date))
            cur.execute(postgre_insert_query, record_to_insert)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            if conn:
                bot.send_message(message.chat.id, "Failed to insert try again")
        finally:
            if conn:
                cur.close()
    elif current_money == "cdollar":
        exchange_result = current_value / cad_price
        bot.send_message(message.chat.id, exchange_result)
        record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                            message.chat.id, datetime.fromtimestamp(message.date))
        try:
            cur.execute(postgre_insert_query, record_to_insert)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            if conn:
                bot.send_message(message.chat.id, "Failed to insert try again")
        finally:
            if conn:
                cur.close()
    else:
        bot.send_message(message.chat.id, "Введите корректные данные.")
    current_value = 0
    current_money = ""
    outro_handler(message.chat.id)


@bot.message_handler(commands=['history'])
def ex_command(message):
    cur = conn.cursor()
    real_id = str(message.chat.id)
    try:
        cur.execute(postgreSQL_select_Query, (real_id,))
        user_records = cur.fetchall()
        result = ""
        for row in user_records:
            result += "Входная валюта: {0}, выходная валюта: {1}, входное значение: {2}, результат: {3}," \
                      "дата: {4}\n".format(row[1], row[2], row[3], row[4], row[7])
        bot.send_message(message.chat.id, result)
    except (Exception, psycopg2.Error) as error:
        bot.send_message(message.chat.id, "Database error")
    finally:
        if conn:
            cur.close()


bot.polling(none_stop=True, interval=0)

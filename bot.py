import telebot
from telebot import types
from util.moneycurs import *
from datetime import datetime
from util.db_connection import *

bot = telebot.TeleBot('1313518366:AAHBOBQXYIY3UYa8IjOvn-r4TPj8oPiwXvI')

current_money = ""
current_value = 0
chat_id = 0


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
        sent = bot.send_message(message.chat.id, "Вы ввели текст. Напишите что-нибудь в чат, чтобы продолжить")
    elif message.content_type == 'photo':
        sent = bot.send_message(message.chat.id, "Вы отправили изображение. Напишите что-нибудь в чат,"
                                                 "чтобы продолжить")
    else:
        sent = bot.send_message(message.chat.id, "Вы отправили что-то другое. Напишите что-нибудь в чат,"
                                                 "чтобы продолжить")
    global chat_id
    chat_id = message.chat.id
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


@bot.message_handler(commands=['exchange'])
def ex_command(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    sent = bot.send_message(message.chat.id, "Введите название нужной валюты(USD Dollar = dollar, Euro = euro, Canadian"
                                             "dollar = cdollar)", reply_markup=hide_markup)
    bot.register_next_step_handler(sent, handle_exchange_valute)


def handle_exchange_valute(message):
    global current_money
    current_money = message.text
    sent = bot.send_message(message.chat.id, "Введите количество рублей для перевода, если значение не целое,"
                                             "то вводите через точку.")
    bot.register_next_step_handler(sent, input_value)


def input_value(message):
    global current_value
    try:
        current_value = float(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Через точку!")
        current_value = None
    global current_money
    dt_object = datetime.fromtimestamp(message.date)
    cur = conn.cursor()
    postgre_insert_query = """ INSERT INTO exchange (INVALUTE, OUTVALUTE, INVALUE, OUTVALUE, USERNAME, CHATID,
        CURDATE) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    if current_value is None:
        sent = bot.send_message(message.chat.id, "Всё неправильно ввёл, давай заново. Напиши что-нибудь в чат,"
                                                 "чтобы продолжить")
    elif current_money == "dollar":
        exchange_result = current_value / usd_price
        sent = bot.send_message(message.chat.id, exchange_result)
        try:
            record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                                message.chat.id, dt_object)
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
        sent = bot.send_message(message.chat.id, exchange_result)
        try:
            record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                                message.chat.id, dt_object)
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
        sent = bot.send_message(message.chat.id, exchange_result)
        record_to_insert = ("RUB", current_money, current_value, exchange_result, message.chat.username,
                            message.chat.id, dt_object)
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
        sent = bot.send_message(message.chat.id, "Введите корректные данные. Напиши, что-нибудь в чат, чтобы"
                                                 "продолжить")
    current_value = 0
    current_money = ""
    global chat_id
    chat_id = message.chat.id
    bot.register_next_step_handler(sent, send_commands)


@bot.message_handler(commands=['history'])
def ex_command(message):
    cur = conn.cursor()
    postgreSQL_select_Query = """ SELECT * FROM EXCHANGE WHERE CHATID = %s"""
    real_id = str(message.chat.id)
    cur.execute(postgreSQL_select_Query, (real_id,))
    user_records = cur.fetchall()
    try:
        for row in user_records:
            invalute = row[1]
            outvalute = row[2]
            invalue = row[3]
            outvalue = row[4]
            data = row[7]
            nmessage = "Входная валюта: {0}, выходная валюта: {1}, входное значение: {2}, результат: {3}," \
                       "дата: {4}".format(invalute, outvalute, invalue, outvalue, data)
            bot.send_message(message.chat.id, nmessage)
    except (Exception, psycopg2.Error) as error:
        bot.send_message(message.chat.id, "Database error")
    finally:
        if conn:
            cur.close()


bot.polling(none_stop=True, interval=0)

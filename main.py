import telebot
from pyowm import owm
from telebot import types
import sqlite3
import random
import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config

import datetime
name = surname = age = ""
##################################   Приветствие   #########################

bot = telebot.TeleBot('5375695745:AAETNH7ETCPxcaESCy6I3HmweyNbd7I3BPY')


first = ["Сегодня — идеальный день для новых начинаний.",
         "Оптимальный день для того, чтобы решиться на смелый поступок!",
         "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
         "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
         "Плодотворный день для того, чтобы разобраться с накопившимися делами."]
second = ["Но помните, что даже в этом случае нужно не забывать про", "Если поедете за город, заранее подумайте про",
          "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
          "Если у вас упадок сил, обратите внимание на",
          "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
second_add = ["отношения с друзьями и близкими.",
              "работу и деловые вопросы, которые могут так некстати помешать планам.",
              "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
              "бытовые вопросы — особенно те, которые вы не доделали вчера.",
              "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
         "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
         "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
         "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
         "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]

###############################  БД    ########################3
@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'hello':
        bot.send_message(message.from_user.id, 'Hi, I am bot, чем тебе помочь ? \n ')
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('погода', callback_data='request1')
        item2 = types.InlineKeyboardButton('гороскоп', callback_data='request2')
        item3 = types.InlineKeyboardButton('регистрация', callback_data='request3')
        markup.add(item1, item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'OK =)', reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Please, say : Привет или Hello')
    elif message.text == 'yes':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        pipl_id = message.chat.id
        cursor.execute(f"SELECT id FROM users_bot WHERE id_numb={pipl_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(message.from_user.id, 'Здорово, как тебя зовут?')
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(message.chat.id, 'Ты уже в моей базе =)')
    elif message.text == '/znak':
        bot.register_next_step_handler(message,goroskop)
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю =(... Напиши /help')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "request3":

        bot.send_message(call.message.chat.id, "Отлично давай начнём регистрацию \n напиши (yes)?")
    elif call.data == "request2":
        bot.send_message(call.message.chat.id, "Напиши свой команду /znak?")
    elif call.data == "zodiac":
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(
            second_add) + ' ' + random.choice(third)
        bot.send_message(call.message.chat.id, msg)
    # elif call.data == 'request1':


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Фамилия ?')
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    age = message.text

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_bot(
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_numb INTEGER, name TEXT, surname TEXT, age INTEGER
    )""")
    connect.commit()
#    pipl_id=message.chat.id
#    cursor.execute(f"SELECT id FROM users_bot WHERE id={pipl_id}")
#    data = cursor.fetchone()
 #   if data is None:
    pipl_id = message.chat.id
    cursor.execute("INSERT INTO users_bot(id_numb,name,surname,age) VALUES(?,?,?,?);",(pipl_id, name, surname, int(age)))
    connect.commit()
    bot.send_message(message.from_user.id, "Cупер мы тебя зарегали")


########################################  гороскоп   #####################################


#@bot.callback_query_handler(func=lambda call: True)
def goroskop(message):

        bot.send_message(message.from_user.id, "OK, сейчас я расскажу тебе гороскоп на сегодня.")
        keyboard = types.InlineKeyboardMarkup()
        key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
        keyboard.add(key_telec)
        key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
        keyboard.add(key_bliznecy)
        key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
        keyboard.add(key_rak)
        key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
        keyboard.add(key_lev)
        key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
        keyboard.add(key_deva)
        key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
        keyboard.add(key_vesy)
        key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
        keyboard.add(key_scorpion)
        key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
        keyboard.add(key_strelec)
        key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
        keyboard.add(key_kozerog)
        key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
        keyboard.add(key_vodoley)
        key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
        keyboard.add(key_ryby)
        bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)



bot.polling()
##############################  погода   ##################################


@bot.callback_query_handler(func=lambda call: True)
def weather(message):
    if call.data == "request1":
        try:
            place = message.text
            config_dict=get_default_config()
            config_dict['language']=['ru']
            owm = OWM("af32a19ff1828831c5815167f671f560", config_dict)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(place)
            w=observation.weather
            t = w.temperatuer('celsius')
            t1=t['temp']
            t2=t['feels_like']
            t3=t['temp_max']
            t4=['temp_min']
            wi=w.wind()['speed']
            pr=w.pressure['pres']

            bot.send_message(message.chat.id, 'В городе '+ str(place)+' температура '+str(t1)+'C \n'+
                         ' ощущается как '+str(t2)+'C '+' максимальная температура '+ str(t3) +'C \n'+
                         ' минимальная температура '+str(t4)+'C'+ ' скорость ветра '+str(wi)+'м/с \n'+
                         ' давление '+ str(pr)+' мм.рт.ст')
        except:
            bot.send_message(message.chat.id,'город не найден')










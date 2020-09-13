# -*- coding: utf-8 -*-

import telebot
import GoogleSheets
from OfferService import *

token_telegram = '541338280:AAH846QL0q6ODETecdot3jR6GCFf5pBpaLg'
token_sheet = '1x5ZVTBTggSjEHWW4SpW_V9ROsRS8Ik_9zwnMNseVQwc'
new_token_sheet = '1Dj37PyQP2_1lAfGgwDYWs4_If84qbEbikT9QGBXkf8k'
credentials = 'sheets.json'  # имя файла с закрытым ключом
# Бот для телеграм
bot = telebot.TeleBot(token_telegram)
# Связь с Google 
sheet = GoogleSheets.GoogleSheet(token_sheet, credentials)
name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
# создание клавиатуры с кнопками
keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
key_btns = ['/проверка', '/заказ', '/поступление', '/обновить_таблицу']
for i in key_btns:
    keyboard.row(i)


# Начало работы бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот для магаза, напиши /help для всех команд')


# Вывод подсказки о проверке размеров
@bot.message_handler(commands=['проверка'])
def check_help(message):
    bot.send_message(message.chat.id, 'Проверка размеров\n'
                                      'Напиши ID, получишь все размеры\n'
                                      'Напиши ID и через пробел размер получишь количество')
    bot.register_next_step_handler(message, check)


# Функция проверки размеров
def check(message):
    data = message.text.split()

    text = sheet.check(data)
    print(text)
    if type(text) is not int:
        bot.send_message(message.chat.id,text)
    else:
        if text == 1:
          bot.send_message(message.chat.id,'ID номер не число')
        elif text == 2:
          bot.send_message(message.chat.id,'Данной вещи с ID номером не существует')
        elif text == 3:
            bot.send_message(message.chat.id,'Нет подходящих размеров')


# Вывод подсказки по работе с функцией заказа
@bot.message_handler(commands=['заказ'])
def offer_help(message):
    # bot.send_message(message.chat.id, 'Команда не рабочая')
    bot.send_message(message.chat.id,'Введите данные покупателя:')
    bot.register_next_step_handler(message,offer_customer)


# Запись данных покупателя
def offer_customer(message):
    customer = message.text
    bot.send_message(message.chat.id,'Вводите вещи с ID и перечисляйте размеры с количеством\n'+
                                    'В конце напишите /end')
    bot.register_next_step_handler(message,offer,customer)


# Функция оформления заказа
def offer(message,customer,offer_list = []):
    text = message.text

    print(text, text == '/end')
    if text == '/end':
        offer_list,non_correct = correct_offer(offer_list)
        if len(non_correct)>0:
            bot.send_message(message.chat.id,'Некорректные вещи:\n'+
                '\n'.join(non_correct))
            

        print(offer_list)
        return None

    data = text.split('\n')
    offer_list+=[item.split() for item in data]
    # Превращаем 0 элементы каждой вещи в целое число
    
        

        
    bot.register_next_step_handler(message,offer,customer,offer_list)
    

# Вывод подсказки по работе с функцией поступления товаров на склад
@bot.message_handler(commands=['поступление'])
def adding_help(message):
    bot.send_message(message.chat.id, 'Команда не рабочая')


@bot.message_handler(commands = ['обновить_таблицу'])
def update_table(message):
    sheet.get_sizes()


# Вывод всех команд
@bot.message_handler(commands=['help','h'])
def help(message):
    bot.send_message(message.chat.id, 'Команды для работы с ботом\n'
                                      '/проверка - нужна для проверки количества размеров\n'
                                      '/заказ - для оформления заказа\n'
                                      '/поступление - нужен для добавления размеров в таблицу', reply_markup=keyboard)


# Убираем доп. кнопки
@bot.message_handler(commands=['rm','remove'])
def remove(message):
    bot.send_message(message.chat.id,'Доп. кнопки убраны',reply_markup = remove)


# Вывод на любой текст подсказки
@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.chat.id)
    if True:
        bot.send_message(message.chat.id, 'Напиши /help для команд',reply_markup = keyboard)



bot.polling()

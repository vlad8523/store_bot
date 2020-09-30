# -*- coding: utf-8 -*-

import telebot
import google_sheets
# from transform_functions import correct_order
from pprint import pprint
import storage
import templates

# Пользователи с разрешенным доступом
known_users = []
# Пользователи администраторы
admin_users = []

# Добавить config
token_telegram = '541338280:AAH846QL0q6ODETecdot3jR6GCFf5pBpaLg'
token_sheet = '1x5ZVTBTggSjEHWW4SpW_V9ROsRS8Ik_9zwnMNseVQwc'
new_token_sheet = '1Dj37PyQP2_1lAfGgwDYWs4_If84qbEbikT9QGBXkf8k'
credentials = 'sheets.json'  # имя файла с закрытым ключом
# Бот для телеграм
bot = telebot.TeleBot(token_telegram)
# Связь с Google 
sheet = google_sheets.GoogleSheet(token_sheet, credentials)
sheet.set_store()
# Хранение данных из таблицы
store = storage.Storage()

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
    sizes = store.get_sizes(data)

    if sizes['error_code'] == 0:
        text = '\n'.join([' = '.join(i) for i in zip(sizes['name_sizes'], sizes['counts'])])

        bot.send_message(message.chat.id, text)
    else:
        # Вывод текста ошибки
        if sizes['error_code'] == 1:
            bot.send_message(message.chat.id, 'ID номер не число')
        elif sizes['error_code'] == 2:
            bot.send_message(message.chat.id, 'Данной вещи с ID номером не существует')
        elif sizes['error_code'] == 3:
            bot.send_message(message.chat.id, 'Нет подходящих размеров')


# Вывод подсказки по работе с функцией заказа
@bot.message_handler(commands=['заказ'])
def order_help(message):
    # bot.send_message(message.chat.id, 'Команда не рабочая')
    bot.send_message(message.chat.id, 'Введите данные покупателя:')
    bot.register_next_step_handler(message, order_customer)


# Запись данных покупателя
def order_customer(message):
    # Словарь для покупателя
    customer = templates.customer.copy()
    # Сохранение имени(Временно)                       
    customer['name'] = message.text

    bot.send_message(message.chat.id, 'Вводите вещи с ID и перечисляйте размеры с количеством\n' +
                     'В конце напишите /end')
    # Запуск оформления заказа
    bot.register_next_step_handler(message, order, customer, order_list=[])


# Функция оформления заказа
def order(message, customer, order_list=[]):
    text = message.text
    # pprint(order_list)
    if text == '/end':
        correct_order, non_correct,values_size,values_order = store.create_order(customer, order_list)
        
        # Придется переделывать create_order тк в случае удаления или изменения элементов необходимо изменять correct_order


        # if len(non_correct) > 0:
        #     bot.send_message(message.chat.id, 'Некорректные вещи:\n' +
        #                      '\n'.join(non_correct))
        # bot.send_message(message.chat.id,'Недостаточное количество')
        # for item in correct_order:
        #     if len(item['not_enough'])>0:
        #         print(str(item['id_item'])+' '+' '.join(item['not_enough']))
        #         bot.send_message(message.chat.id,str(item['id_item'])+' '+' '.join(item['not_enough']))
        
        if (len(values_order) == 1):
            bot.send_message(message.chat.id,'Не сделано')
            return None
        sheet.write_order(values_size,values_order)
        # pprint(correct_order_list)

        bot.send_message(message.chat.id,'Сделано')
        # sheet.write_order(values)
        return None

    data = text.split('\n')
    order_list += [item.split() for item in data]
    # Запуск заново функции с передачей сохраненного листа заказа
    bot.register_next_step_handler(message, order, customer=customer, order_list=order_list)


# Вывод подсказки по работе с функцией поступления товаров на склад
@bot.message_handler(commands=['поступление'])
def adding_help(message):
    bot.send_message(message.chat.id, 'Команда не рабочая')


@bot.message_handler(commands=['обновить_таблицу'])
def update_table(message):
    bot.send_message(message.chat.id, 'Пока не работает')
    # sheet.get_sizes()


# Вывод всех команд
@bot.message_handler(commands=['help', 'h'])
def help(message):
    bot.send_message(message.chat.id, 'Команды для работы с ботом\n'
                                      '/проверка - нужна для проверки количества размеров\n'
                                      '/заказ - для оформления заказа\n'
                                      '/поступление - нужен для добавления размеров в таблицу', reply_markup=keyboard)


# Убираем доп. кнопки
@bot.message_handler(commands=['rm', 'remove'])
def remove(message):
    bot.send_message(message.chat.id, 'Доп. кнопки убраны', reply_markup=remove)


# Вывод на любой текст подсказки
@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.chat.id)
    if True:
        bot.send_message(message.chat.id, 'Напиши /help для команд', reply_markup=keyboard)


bot.polling()

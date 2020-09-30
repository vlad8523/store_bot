from telebot import *
import google_sheets


# Пользователи с разрешенным доступом
known_users = []
# Пользователи администраторы
admin_users = [525406830]

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

bot = TeleBot(token_telegram)


# Начало работы бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот для магаза, напиши /help для всех команд')


# Вывод всех команд
@bot.message_handler(commands=['help', 'h'])
def help(message):
    bot.send_message(message.chat.id, 'Команды для работы с ботом\n'
                                      '/проверка - нужна для проверки количества размеров\n'
                                      '/заказ - для оформления заказа\n'
                                      '/поступление - нужен для добавления размеров в таблицу', reply_markup=keyboard)

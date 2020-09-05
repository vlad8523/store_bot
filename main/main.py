import telebot
import GoogleSheets

token_telegram = '541338280:AAH846QL0q6ODETecdot3jR6GCFf5pBpaLg'
token_sheet = '1F_IpnBCt0zwwHm3gkEL3wz6GSLJZ0IV_2-HegqL5bIY'
new_token_sheet = '1Dj37PyQP2_1lAfGgwDYWs4_If84qbEbikT9QGBXkf8k'
credentials = 'sheets.json'  # имя файла с закрытым ключом

bot = telebot.TeleBot(token_telegram)

sheet  = GoogleSheets.GoogleSheet(new_token_sheet,credentials)
name_sizes = ['M','L','XL','2XL','3XL','4XL']

keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
key_btns = ['/проверка','/заказ','/поступление']
for i in key_btns:
    keyboard.row(i)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот для магаза, напиши /help для всех команд')

# Вывод подсказки
@bot.message_handler(commands=['проверка'])
def check_help(message):
    bot.send_message(message.chat.id, 'Проверка размеров\n'
                                      'Напиши ID, получишь все размеры\n'
                                      'Напиши ID и через пробел размер получишь количество')
    bot.register_next_step_handler(message, check)

#
def check(message):
    text = message.text.split()
    id_item = int(text[0])
    size = ''
    if len(text) == 2:
        size = text[1]
        counts = sheet.check(id_item, size)
        text = size.upper() + ' = ' + counts
        bot.send_message(message.chat.id, text)
    else:
        counts = sheet.check(id_item)
        t = [' = '.join(i) for i in zip(name_sizes,counts)]
        text = '\n'.join(t)
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['заказ'])
def offer_help(message):
    bot.send_message(message.chat.id, 'Команда не рабочая')


@bot.message_handler(commands=['поступление'])
def adding_help(message):
    bot.send_message(message.chat.id,'Команда не рабочая')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Команды для работы с ботом\n'
                                      '/проверка - нужна для проверки количества размеров\n'
                                      '/заказ - для оформления заказа\n'
                                      '/поступление - нужен для добавления размеров в таблицу',reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.chat.id)
    if True:
        bot.send_message(message.chat.id,'Напиши /help для команд')


bot.polling()


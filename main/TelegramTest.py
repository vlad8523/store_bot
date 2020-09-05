import telebot

token_telegram = '541338280:AAH846QL0q6ODETecdot3jR6GCFf5pBpaLg'

bot = telebot.TeleBot(token_telegram)

keyboard = telebot.types.ReplyKeyboardMarkup()
buttons = ['Проверить размеры','Заказ','Поступление']
[keyboard.row(i) for i in buttons]

remove = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот для магаза, напиши /help для всех команд', reply_markup=keyboard)


@bot.message_handler(commands=['проверка'])
def check_help(message):
    bot.send_message(message.chat.id, 'Проверка размеров\n'
                                      'Напиши ID, получишь все размеры\n'
                                      'Напиши ID и через пробел размер получишь количество')
    # bot.register_next_step_handler(message, check)




@bot.message_handler(commands=['help'])
def check(message):
    bot.send_message(message.chat.id,'Команды для работы с ботом\n'
                                     '\проверка - нужна для проверки количества размеров\n'
                                     '\заказ - для оформления заказа\n'
                                     '\поступление - нужен для добавления размеров в таблицу')
#
#
# @bot.message_handler(commands=['показать'])
# def show(message):
#     print('show')

@bot.message_handler(content_types=['text'])
def send_text(message):
    # bot.send_message(message.chat.id, 'Это из первого ' + message.text)
    # bot.register_next_step_handler(message, second)
    if message.text == False:
        bot.send_message(message.chat.id,'Напиши /help для команд')

def second(message):
    bot.send_message(message.chat.id,'Это из второго '+message.text)


bot.polling()

from config import *
import transform_functions as tf

correct_order = []
customer = []


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
        correct_order, non_correct = store.get_correct_order(order_list)
        
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


@bot.callback_query_handler(lambda call: call.data == 'change_order')
def call_change_order(call):
    


@bot.callback_query_handler(lambda call: call.data.split('_')[0]=='order')
def call_order(call):
    command = call.data.split('_')[1]
    if command == 'apply':
        values_order = tf.create_values_order(customer, correcr_order)
        values_sizes = store.get_sizes()['counts']
        sheet.write_order(values_size,values_order)
        bot.send_message(call.message.chat.id,"Сделан")
        return None

    if command == 'cancel':



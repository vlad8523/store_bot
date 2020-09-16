def correct_order(order_list):
    '''
    Создает корректный заказ
    Возращает лист с корректным заказом и некорректными элементами
    '''


    name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
    size_dict = {size: 0 for size in name_sizes}

    non_correct_items = []
    for i in range(len(order_list))[::-1]:
        # Проверка на id вещи
        # Не сделано проверка на наличие в таблицу!!!
        if order_list[i][0].isdigit():
            order_list[i] = [int(order_list[i][0])] + order_list[i][1:]
            # Проверка на вид заказа id,(размер,количество)*
            if len(order_list[i]) % 2 != 1:
                non_correct_items.append(order_list.pop(i))
        else:
            non_correct_items.append(order_list.pop(i))

    for i in range(len(order_list)):
        # Временный id, некорректные размеры и лист для размеров вида [[size,counts],...,[size,counts]]
        tmp_id = order_list[i][0]
        tmp_failed = []
        tmp_sizes_zip = []
        # Корректный список заказов(хранит в себе все вещи в виде словаря с id, размерами и некорректными размерами)
        correct_order_list = []

        for j in range(len(order_list[i]))[1::2]:
            # Временный размер и количество
            tmp_size = order_list[i][j].upper()
            tmp_count = order_list[i][j + 1]

            if tmp_size in name_sizes:
                if tmp_count.isdigit():
                    tmp_sizes_zip.append([tmp_size, tmp_count])
                else:
                    tmp_failed.append(tmp_size)
                    continue
            else:
                tmp_failed.append(tmp_size)
                continue

        correct_order_list.append({
            'id_item': tmp_id,
            'sizes': tmp_sizes_zip,
            'failed': tmp_failed
        })

    return [correct_order_list, non_correct_items[::-1]]


# Создает значение для вставки в таблицу
# Не все элементы пока вставляются!!!
def create_values(customer, order_list):
    # Ключи для словаря покупателя
    customer_keys = ['number_offer', 'name', 'date', 'delivery', 'phone', 'address']

    # order_values хранит в себе значения всех купленных вещей для вставки 
    order_values = []
    # Хранит в себе значения покупателя для вставки
    customer_values = [[customer[key] for key in customer_keys] + [''] * 6]

    for item in order_list:
        for size in item['sizes']:
            ls = ([''] * 6) + [''] + [item['id_item']] + [''] + size + ['']
            order_values.append(ls)

    values = customer_values + order_values
    return values


def create_storage(raw_data):
    storage = []

    for row in raw_data:
        storage.append({
            'id_item': row[0],
            'type': row[1],
            'name': row[2],
            'color': row[3],
            'price': row[7],
            'sizes': row[8:]
        })

    return storage

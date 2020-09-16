name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']


def correct_order(store, order_list):
    '''
    Создает корректный заказ
    Возращает лист с корректным заказом и некорректными элементами

    :param order_list:
    :return:
    '''

    size_dict = {size: 0 for size in name_sizes}

    non_correct_items = []
    correct_order_list = []

    for i in range(len(order_list))[::-1]:
        # Проверка на id вещи
        # Не сделано проверка на наличие в таблицу!!!
        if order_list[i][0].isdigit():
            tmp_id = int(order_list[i][0])

            order_list[i] = [tmp_id] + order_list[i][1:]
            # Проверка на вид заказа id,(размер,количество)*

            if len(order_list[i]) % 2 != 1:
                non_correct_items.append(order_list.pop(i))

            current_counts = store.get_sizes([str(tmp_id)])

            if current_counts['error_code'] != 0:
                non_correct_items.append(order_list.pop(i))

        else:
            non_correct_items.append(order_list.pop(i))

    correct_counts_fun = lambda x,y: int(x)<=int(y)

    for i in range(len(order_list)):
        # Временный id, некорректные размеры и лист для размеров вида [[size,counts],...,[size,counts]]
        tmp_id = order_list[i][0]

        tmp_sizes_zip = [[size.upper(), counts] for size, counts in zip(order_list[i][1::2], order_list[i][2::2]) if
                         (size.upper() in name_sizes) and (counts.isdigit())]
        tmp_failed = [size.upper() for size, counts in zip(order_list[i][1::2], order_list[i][2::2]) if
                      (size.upper() not in name_sizes) or (not counts.isdigit())]
        tmp_sizes = [size for size, counts in tmp_sizes_zip]
        tmp_counts = [counts for size, counts in tmp_sizes_zip]

        tmp_not_enough = []
        data = [str(tmp_id)]+tmp_sizes

        curr_counts = store.get_sizes(data)['counts']

        cond_counts = [correct_counts_fun(x,y) for x,y in zip(tmp_counts,curr_counts)]

        for j in range(len(tmp_sizes_zip))[::-1]:
            if not cond_counts[j]:
                del tmp_sizes_zip[j]
                tmp_not_enough.append(tmp_sizes.pop(j))
        # Корректный список заказов(хранит в себе все вещи в виде словаря с id, размерами и некорректными размерами)

        correct_order_list.append({
            'id_item': tmp_id,
            'sizes': tmp_sizes_zip,
            'failed': tmp_failed,
            'not_enough': tmp_not_enough
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
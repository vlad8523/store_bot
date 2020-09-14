def correct_order(order_list):
    name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
    size_dict = {size: 0 for size in name_sizes}

    non_correct_items = []
    for i in range(len(order_list))[::-1]:
        if order_list[i][0].isdigit():
            order_list[i] = [int(order_list[i][0])] + order_list[i][1:]
        else:
            non_correct_items.append(order_list.pop(i))
    for i in range(len(order_list)):
        tmp_id = order_list[i][0]
        tmp_failed = []
        tmp_sizes_zip = []
        if len(order_list[i]) % 2 == 1:

            for j in range(len(order_list[i]))[1::2]:

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
        order_list[i] = {
            'id_item': tmp_id,
            'sizes': list(map(list, tmp_sizes_zip)),
            'failed': tmp_failed
        }

    return [order_list, non_correct_items[::-1]]


def create_values(customer, offer_list):
    customer_keys = ['number_offer', 'name', 'date', 'delivery', 'phone', 'address']

    array = []
    offer = [[customer[key] for key in customer_keys] + [''] * 6]
    for item in offer_list:
        for size in item['sizes']:
            ls = ([''] * 6) + [''] + [item['id_item']] + [''] + size + ['']
            array.append(ls)

    offer += array
    return offer

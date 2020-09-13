from pprint import pprint

offer_list = [[1, 'l', '2', '2xl', '3'], ['О'], [5, '3xl', '5', 'l', '2'], [9, 'm', '5', 'l', 'xl', '1']]

offer = '1 l 2 2xl 3\nО атвту\n5 3xl 5 l 2\n9 s 5 l 1'.split('\n')
offer = [item.split() for item in offer]


def correct_offer(offer_list):
    name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
    size_dict = {size: 0 for size in name_sizes}

    non_correct_items = []
    for i in range(len(offer_list))[::-1]:
        if offer_list[i][0].isdigit():
            offer_list[i] = [int(offer_list[i][0])] + offer_list[i][1:]
        else:
            non_correct_items.append(offer_list.pop(i))
    for i in range(len(offer_list)):
        tmp_id = offer_list[i][0]
        tmp_failed = []
        tmp_sizes_zip = []
        if len(offer_list[i]) % 2 == 1:

            for j in range(len(offer_list[i]))[1::2]:

                tmp_size = offer_list[i][j].upper()
                tmp_count = offer_list[i][j + 1]

                if tmp_size in name_sizes:
                    if tmp_count.isdigit():
                        tmp_sizes_zip.append(list(zip(tmp_size, tmp_count))[0])
                    else:
                        tmp_failed.append(tmp_size)
                        continue
                else:
                    tmp_failed.append(tmp_size)
                    continue
        offer_list[i] = {
            'id_item': tmp_id,
            'sizes': list(map(list, tmp_sizes_zip)),
            'failed': tmp_failed
        }

    return [offer_list, non_correct_items[::-1]]


def create_offer(customer, offer_list):
    customer_keys = ['number_offer', 'name', 'date', 'delivery', 'phone', 'address']

    array = []
    offer = [[customer[key] for key in customer_keys] + [''] * 6]
    for item in offer_list:
        for size in item['sizes']:
            ls = ([''] * 6) + [''] + [item['id_item']] + [''] + size + ['']
            array.append(ls)

    offer += array
    return offer

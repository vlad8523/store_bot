import copy

sizes = {
    'name_sizes': [],
    'counts': [],
    'failed': [],
    'error_code': 0
}

customer = {'number_offer': '',
            'name': '',
            'date': '',
            'delivery': '',
            'phone': '',
            'address': ''}

order_item = {
    'customer': copy.deepcopy(customer),
    'order_list': []
}

import copy

name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']

sizes_counts = {key: 0 for key in name_sizes}

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
    'order': {}
}

order = {
    'list_IDs': [],
    'dict_order': {},
}

ID_order_item = {
    'sizes': copy.deepcopy(sizes_counts),
    'failed': []
}

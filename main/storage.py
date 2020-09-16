from transform_functions import *
import templates


# Хранит в себе все значения из таблицыБ и производит манипуляции с данными
class Storage:

    ___shared_state = {}

    sizes_list = []
    storage_list = []

    order_list = []

    def __init__(self):
        self.__dict__ = self.___shared_state

        self.name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']

    def set_storage(self, raw_storage):
        self.storage_list = create_storage(raw_storage)

    def set_sizes(self):
        sizes_list = []

        for item in self.storage_list:
            sizes_list.append(item['sizes'])

        self.sizes_list = sizes_list

    def set_order(self, raw_orders):
        self.order_list = raw_orders

    def get_storage(self):
        return self.storage_list

    def get_sizes(self, data=''):

        sizes = templates.sizes.copy()

        if data == '':
            sizes['counts'] = self.sizes_list
            return sizes

        if data[0].isdigit():
            id_item = int(data[0]) - 1

        else:
            sizes['error_code'] = 1
            return sizes
        # Проверка ID
        if id_item >= len(self.sizes_list) or id_item < 0:
            sizes['error_code'] = 2
            return sizes

        if len(data) >= 2:

            for size in data[1:]:
                print(size)
                if size.upper() in self.name_sizes:
                    sizes['name_sizes'].append(size.upper())
                    sizes['counts'].append(self.sizes_list[id_item][self.name_sizes.index(size.upper())])
                    # Если не было подходящих размеров из data
                else:
                    sizes['failed'].append(size)
            if len(sizes['counts']) == 0:
                sizes['error_code'] = 3
                return sizes
        else:
            counts = self.sizes_list[id_item]

            sizes['name_sizes'] = self.name_sizes
            sizes['counts'] = counts

        return sizes

    def get_order_list(self):
        return self.order_list

    def create_order(self, customer, order_list):
        values = create_values(customer, order_list)

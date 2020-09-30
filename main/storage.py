from transform_functions import *
import templates
from pprint import pprint
import copy


# Хранит в себе все значения из таблицы и производит манипуляции с данными
class Storage:
    ___shared_state = {}

    # Складской лист
    sizes_list = [[]]
    storage_list = [[]]

    order_list = []

    name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
    sizes_dict = {name_sizes[i]:i for i in range(len(name_sizes))}

    def __init__(self):
        # Необходимо для monostate
        self.__dict__ = self.___shared_state

    def set_storage(self, raw_storage):
        self.storage_list = create_storage(raw_storage)
        self.set_sizes()

    def set_sizes(self):
        '''
        Вытаскивает все размеры из листа размеров
        '''
        sizes_list = []

        for item in self.storage_list[1:]:
            sizes_list.append(item['sizes'])

        self.sizes_list += sizes_list


    def set_order(self, raw_orders):
        # Временное решение 
        # Придумать парсинг всех заказов и разделение данных среди переменных
        self.order_list = raw_orders

    def update_sizes(self,order):
        '''
        Обновляет таблицу размеров согласно заказу
        '''

        for item in order:
            id_item = item['id_item']
            sizes_zip = item['sizes']

            data = [id_item]

            cur_sizes = [int(i) for i in self.get_sizes(data)['counts']]

            for size in sizes_zip:
                cur_sizes[self.sizes_dict[size[0]]] -= int(size[1])

            cur_values_size = [str(i) for i in cur_sizes]

            # Обновление данных внутри storage
            self.sizes_list[id_item] = cur_values_size
            self.storage_list[id_item]['sizes'] = cur_values_size

    def get_storage(self):
        return self.storage_list

    def get_sizes(self, data=None):
        if data is None:
            data = []

        sizes = copy.deepcopy(templates.sizes)
        pprint(templates.sizes)
        if len(data) == 0:
            sizes['counts'] = self.sizes_list[1:]
            return sizes

        if type(data[0]) is int:
            id_item = data[0]
        elif data[0].isdigit():
            id_item = int(data[0])

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

    def get_correct_order(self,order_list):
        correct_order, non_correct = create_correct_order(self, order_list)

        return correct_order, non_correct

    def create_order(self, customer, order_list):
        '''
        Функция создания заказа
        '''
        order, non_correct = create_correct_order(self, order_list)
        self.update_sizes(order)
        # Создание значений для вставки в таблицу
        values_order = create_values_order(customer, order)
        values_sizes = self.get_sizes()['counts']

        return order, non_correct, values_sizes, values_order

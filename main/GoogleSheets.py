# -*- coding: utf-8 -*-

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


class GoogleSheet:

    def __init__(self, token, credentials):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials,
                                                                            [
                                                                                'https://www.googleapis.com/auth/spreadsheets',
                                                                                'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.store = ['Склад', 'МПродажи']
        self.token = token

        # self.titles = self.get_titles()

        self.name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
        self.range_size = [self.store[0] + '!J7:O']
        self.range_orders = [self.store[1] + '!B7:M']

        self.get_sizes()
        self.get_orders()

    def get_titles(self):
        """
        Получает названия всех листов таблице
        """
        results = self.service.spreadsheets().get(spreadsheetId=self.token).execute()
        titles = [sheet['properties']['title'] for sheet in results['sheets']]
        return titles

    def get(self, range):
        """
        Получает данные с выбранного диапазона и возвращает его

        """
        results = self.service.spreadsheets().values().batchGet(spreadsheetId=self.token,
                                                                ranges=range,
                                                                valueRenderOption='FORMATTED_VALUE').execute()
        return results

    def get_sizes(self):
        """
        Подгружает размеры из табли Google

        """
        results = self.get(self.range_size)

        self.sizes = results['valueRanges'][0]['values']

    def get_orders(self):
        '''

        :return:
        '''
        results = self.get(self.range_orders)

        self.orders = results['valueRanges'][0]['values']

    def write(self, range, values):
        """
        Обновляет таблицу в выбранном диапазоне

        """
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.token,
                                                         body={
                                                             "valueInputOption": "USER_ENTERED",
                                                             "data": [
                                                                 {"range": range,
                                                                  "majorDimension": "ROWS",
                                                                  "values": values}]
                                                         }).execute()

    def write_sizes(self, values=''):
        """
        Обновляет таблицу в диапазоне размеров

        """
        if values == '':
            self.write(self.range_size, self.sizes)
        else:
            self.write(self.range_size, values)

    def write_order(self, values):
        range = 'МПродажи!B' + str(7 + len(self.orders)) + ':M'
        self.orders+=values
        self.write(range, values)

    # сделать одну функцию с check_size
    def check(self, data):
        """
        Функция проверки размеров

        :param id_item: ID вещи в таблице
        :param size: размер вещи, если пусто, то выводит все размеры
        :return:
        """
        # Проверка на число
        if data[0].isdigit():
            id_item = int(data[0]) - 1
        else:
            return 1
        # Проверка на превышение ID
        if id_item >= len(self.sizes):
            return 2

        sizes = {
            'name_sizes': [],
            'counts': []
        }

        if len(data) >= 2:

            for size in data[1:]:
                print(size)
                if size.upper() in self.name_sizes:
                    sizes['name_sizes'].append(size.upper())
                    sizes['counts'].append(self.sizes[id_item][self.name_sizes.index(size.upper())])
                    # Если не было подходящих размеров из data
            if len(sizes['counts']) == 0:
                return 3
        else:
            counts = self.sizes[id_item]

            sizes['name_sizes'] = self.name_sizes
            sizes['counts'] = counts

        return sizes

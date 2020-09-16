# -*- coding: utf-8 -*-

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import storage


class GoogleSheet:
    store = storage.Storage()
    store_titles = ['Склад', 'МПродажи']

    range_storage = store_titles[0] + '!B7:O'
    range_sizes = store_titles[0] + '!J7:O'
    range_orders = store_titles[1] + '!B7:M'
    range_store = [range_storage, range_orders]

    def __init__(self, token, credentials):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials,
                                                                            [
                                                                                'https://www.googleapis.com/auth/spreadsheets',
                                                                                'https://www.googleapis.com/auth/drive'])

        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

        self.token = token

        # self.titles = self.get_titles()

    def get_titles(self):
        """
        Получает названия всех листов таблицы
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
        return results['valueRanges']

    def get_store(self):
        results = self.get(self.range_store)
        return results

    def get_storage(self):
        '''
        Получает все значения со склада

        '''
        raw_storage = self.get([self.range_storage])[0]['values']

        return raw_storage

    def get_orders(self):
        '''
        Получает все значения заказов
        :return:
        '''
        results = self.get([self.range_orders])[0]['values']

        return results

    def write(self, data):
        """
        Обновляет таблицу в выбранном диапазоне

        """
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.token,
                                                         body={
                                                             "valueInputOption": "USER_ENTERED",
                                                             "data": data
                                                         }).execute()

    def write_sizes(self, values=''):
        """
        Обновляет таблицу в диапазоне размеров

        """
        data = [
            {"range": self.range_sizes,
             "majorDimensions": "ROWS",
             "values": values
             }]

        self.write(data=data)

    def write_order(self, sizes, order_list):
        '''
        Записывает данные заказа в таблицу

        '''
        range_order_list = 'МПродажи!B' + str(7 + len(self.store.get_order_list())) + ':M'

        data = [
            {
                "range": self.range_sizes,
                "majorDimension": "ROWS",
                "values": sizes
            },
            {
                "range": range_order_list,
                "majorDimension": "ROWS",
                "values": order_list
            }]

        self.write(data)

    def update_orders(self, values):
        return None

    def set_store(self):
        storage_lists = self.get_store()

        self.store.set_storage(storage_lists[0]['values'])
        self.store.set_sizes()
        self.store.set_order(storage_lists[1]['values'])

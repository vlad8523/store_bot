# -*- coding: utf-8 -*-

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import storage


# Переместить функ


class GoogleSheet:

    def __init__(self, token, credentials):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials,
                                                                            [
                                                                                'https://www.googleapis.com/auth/spreadsheets',
                                                                                'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.store_titles = ['Склад', 'МПродажи']
        self.token = token

        # self.titles = self.get_titles()

        self.name_sizes = ['M', 'L', 'XL', '2X"L', '3XL', '4XL']
        self.range_orders = [self.store_titles[1] + '!B7:M']
        self.range_store = [self.store_titles[0] + '!B7:O']
        self.range_storage = [self.range_store,self.range_orders]

        self.storage = storage.Storage()

        storage_lists = self.get_storage()

        self.storage.set_storage(storage_lists[0]['values'])
        self.storage.set_sizes()

        self.storage.set_order(storage_lists[1]['values'])



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
        return results

    def get_storage(self):
        results = self.service.spreadsheets().values().get(spreadsheetId=self.token,
                                                                ranges=self.range_storage,
                                                                valueRenderOption='FORMATTED_VALUE').execute()

        return results['valueRanges']

    def get_store(self):
        '''
        Получает все значения со склада

        '''
        raw_storage = self.get(self.range_store)

        return raw_storage['valueRanges'][0]['values']

    def get_orders(self):
        '''
        Получает все значения заказов
        :return:
        '''
        results = self.get(self.range_orders)

        return results['valueRanges'][0]['values']

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

    def update_sizes(self, values=''):
        """
        Обновляет таблицу в диапазоне размеров

        """
        if values == '':
            self.write(self.range_size, self.sizes)
        else:
            self.write(self.range_size, values)

    def write_order(self, values):
        '''
        Записывает данные заказа в таблицу

        '''

        # range = 'МПродажи!B' + str(7 + len(self.orders)) + ':M'
        # self.orders += values
        #
        # self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.token,
        #                                                  body={
        #                                                      "valueInputOption": "USER_ENTERED",
        #                                                      "data": [
        #                                                          {"range": range,
        #                                                           "majorDimension": "ROWS",
        #                                                           "values": values}]
        #                                                  }).execute()

    def update_orders(self, values):
        return None
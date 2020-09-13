# -*- coding: utf-8 -*-

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:

    def __init__(self, token, credentials):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials,
                                                                            [
                                                                                'https://www.googleapis.com/auth/spreadsheets',
                                                                                'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.store = ['Склад', 'Заказы']
        self.token = token

        # self.titles = self.get_titles()
        
        self.name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
        self.range_size = [self.store[0] + '!J7:O']
        self.get_sizes()


    # def offer(self,customer,offer = []):
    #     failed_items = []
    #     for item in range(len(offer)):
    #         
    #     pass

    def get_titles(self):
        """
        Получает названия всех листов таблице
        """
        results = self.service.spreadsheets().get(spreadsheetId = self.token).execute()
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


    def update(self, range, values):
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
    

    def get_sizes(self):
        """
        Подгружает размеры из табли Google

        """
        results = self.get(self.range_size)

        self.sizes = results['valueRanges'][0]['values']


    def update_sizes(self):
        """
        Обновляет таблицу в диапазоне размеров

        """
        self.update(self.range_size, self.sizes)


    # сделать одну функцию с check_size
    def check(self,data):
        """
        Функция проверки размеров

        :param id_item: ID вещи в таблице
        :param size: размер вещи, если пусто, то выводит все размеры
        :return:
        """
        # Проверка на число
        if data[0].isdigit():
            id_item = int(data[0])-1
        else:
            return 1
        # Проверка на превышение ID
        if id_item >= len(self.sizes):
                return 2

        if len(data) >= 2:
            counts = []
            for size in data[1:]:
                if size.upper() in self.name_sizes:
                    counts.append(size.upper()+' = '+
                        self.sizes[id_item][self.name_sizes.index(size.upper())])
            # Если не было подходящих размеров из data
            if len(counts)==0:
                return 3
        else:
            counts = self.sizes[id_item]
            counts = [' = '.join(i) for i in zip(self.name_sizes, counts)]
            
        text = '\n'.join(counts)
        return text
        
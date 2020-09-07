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
        self.store = ['Закуп', 'Склад', 'Заказы']
        self.token = token

        self.name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
        self.range_size = [self.store[0] + '!J7:O35']
        self.get_sizes()


    def get(self, range):
        """
        Получает данные с выбранного диапозона и возвращает его

        """
        results = self.service.spreadsheets().values().batchGet(spreadsheetId=self.token,
                                                                ranges=range,
                                                                valueRenderOption='FORMATTED_VALUE').execute()
        return results


    def update(self, range, values):
        """
        Обновляет таблицу в выбранном диапозоне

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
        Обновляет таблицу в диапозоне размеров

        """
        self.update(self.range_size, self.sizes)

    # сделать одну функцию с check_size
    def check(self,data):
        # Проверка на число
        if data[0].isdigit():
            id_item = int(data[0])
        else:
            return 1

        if len(text) >= 2:
            size = text[1]
            text = sheet.check(id_item, data[1:])
        else:
            counts = sheet.check(id_item)
            t = [' = '.join(i) for i in zip(name_sizes, counts)]
            text = '\n'.join(t)
        return text


    def check_size(self, id_item, sizes=''):
        """
        Функция проверки размеров

        :param id_item: ID вещи в таблице
        :param size: размер вещи, если пусто, то выводит все размеры
        :return:
        """
        if id_item >= len(self.sizes):
                return 2
        if size == '':
            return self.sizes[id_item]
        else:
            text = ''
            for size in sizes:
                for i in range(len(self.name_sizes)):
                    if size.lower() == self.name_sizes[i].lower():
                        text += size.upper()+' = '+self.sizes[id_item][i]+'\n'
                        break
            return text

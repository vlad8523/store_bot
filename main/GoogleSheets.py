import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:

    def __init__(self,token,credentials):
        CREDENTIALS_FILE = credentials

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.store = ['Закуп','Склад', 'Заказы']
        self.token = token

        self.name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']
        self.range_size = [self.store[0]+'!J7:O35']
        self.get_sizes()


    def get(self,range):
        results = self.service.spreadsheets().values().batchGet(spreadsheetId=self.token,
                                                           ranges=range,
                                                           valueRenderOption='FORMATTED_VALUE').execute()
        return results

    def update(self,range, values):
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.token,
                                                    body={
                                                        "valueInputOption": "USER_ENTERED",
                                                        "data": [
                                                            {"range": range,
                                                             "majorDimension": "ROWS",
                                                             "values": values}]
                                                    }).execute()

    def get_sizes(self):
        results = self.get(self.range_size)

        self.sizes = results['valueRanges'][0]['values']



    def update_sizes(self):
        self.update(self.range_size,self.sizes)

    def check(self,id_item,size = ''):
        """
        Функция проверки размеров

        :param id_item: ID вещи в таблице
        :param size: размер вещи, если пусто, то выводит все размеры
        :return:
        """
        if size == '':
            if id_item>=len(self.sizes):
                return 1
            return self.sizes[id_item]
        else:
            for i in range(len(self.name_sizes)):
                if size.lower() == self.name_sizes[i].lower():
                    return self.sizes[id_item][i]
            return 2
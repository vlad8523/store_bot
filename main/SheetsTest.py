import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

token = '1F_IpnBCt0zwwHm3gkEL3wz6GSLJZ0IV_2-HegqL5bIY'

credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets.json',
                                                               [
                                                                   'https://www.googleapis.com/auth/spreadsheets',
                                                                   'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
#
results = service.spreadsheets().get(spreadsheetId='1F_IpnBCt0zwwHm3gkEL3wz6GSLJZ0IV_2-HegqL5bIY').execute()
titles = [sheet['properties']['title'] for sheet in results['sheets']]
pprint(results)
# print(titles)
# service.spreadshee ts().batchUpdate(spreadsheetId='1F_IpnBCt0zwwHm3gkEL3wz6GSLJZ0IV_2-HegqL5bIY', body={
#   "requests": [
#     {
#       "updateSheetProperties": {
#         "fields": "title",
#         "properties": {
#           "title": "qwertt",
#           "sheetId": 0
#         }
#       }
#     }
#   ]
# }).execute()
# pprint(results)
# print(titles)

from gsuite.GSuite import GSuite
from gsuite.GDrive import GDrive
from utils.Dev import Dev


class GSheets:

    def __init__(self, gsuite_secret_id=None):
        self.gdrive       = GDrive(gsuite_secret_id)
        self.spreadsheets = GSuite(gsuite_secret_id).sheets_v4().spreadsheets()

    def batch_update(self, file_id, requests):
        body = {'requests': requests  }
        return self.execute(self.spreadsheets.batchUpdate(spreadsheetId=file_id, body=body))

    def execute(self,command):
        return self.gdrive.execute(command)

    def execute_request(self, sheet_id, request):
        return self.batch_update(sheet_id, [request])

    def execute_requests(self, sheet_id, requests):
        return self.batch_update(sheet_id, requests)


    def all_spreadsheets(self):
        mime_type_presentations = 'application/vnd.google-apps.spreadsheet'
        return self.gdrive.find_by_mime_type(mime_type_presentations)

    def sheets_metadata(self, file_id):
        return self.execute(self.spreadsheets.get(spreadsheetId=file_id))

    def sheets_add_sheet(self, file_id, title):
        request = { "addSheet": { "properties": { "title": title } } }

        result  =  self.execute_request(file_id, [request])
        return result.get('replies')[0].get('addSheet').get('properties').get('sheetId')


    def sheets_delete_sheet(self, file_id, sheet_id):
        request = { "deleteSheet": { "sheetId": sheet_id } }

        return self.execute_request(file_id, [request])

    def sheets_rename_sheet(self, file_id, sheet_id, new_name):
        request = {"updateSheetProperties": { "properties": { "sheetId": sheet_id    ,
                                                              "title"  : new_name   },
                                              "fields"    :   "title"               }}
        return self.execute_request(file_id, [request])

    def sheets_properties_by_id(self, file_id):
        values = {}
        metadata = self.sheets_metadata(file_id)
        for sheet in metadata.get('sheets'):
           properties = sheet.get('properties')
           sheet_id   = properties.get('sheetId')
           values[sheet_id] = properties
        return values

    def sheets_properties_by_title(self, file_id):
        values = {}
        metadata = self.sheets_metadata(file_id)
        for sheet in metadata.get('sheets'):
           properties = sheet.get('properties')
           sheet_id   = properties.get('title')
           values[sheet_id] = properties
        return values

    def clear_values(self, file_id, sheet_name):
        sheet_range = "{0}!A1:Z".format(sheet_name)
        return self.execute(self.spreadsheets.values().clear(spreadsheetId=file_id, range=sheet_range))

    def get_values(self, file_id, range):
        values = self.spreadsheets.values()
        result = self.execute(values.get(spreadsheetId = file_id , range = range    ))
        return result.get('values')

    def set_values(self, file_id, sheet_range, values):
        value_input_option = 'RAW' # vs USER_ENTERED
        body               = { 'values' : values }
        result = self.execute(self.spreadsheets.values().update( spreadsheetId    = file_id,
                                                                 range            = sheet_range,
                                                                 valueInputOption = value_input_option,
                                                                 body             = body))
        return result


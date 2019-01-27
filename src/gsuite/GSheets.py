from gsuite.GSuite import GSuite
from gsuite.GDrive import GDrive
from utils.Dev import Dev


class GSheets:

    def __init__(self):
        self.gdrive       = GDrive()
        self.spreadsheets = GSuite().sheets_v4().spreadsheets()

    def batch_update(self, sheet_id, requests):
        body = {'requests': requests  }
        return self.execute(self.spreadsheets.batchUpdate(spreadsheetId=sheet_id, body=body))

    def execute(self,command):
        return self.gdrive.execute(command)

    def execute_requests(self, sheet_id, requests):
        return self.batch_update(sheet_id, requests)


    def all_spreadsheets(self):
        mime_type_presentations = 'application/vnd.google-apps.spreadsheet'
        return self.gdrive.find_by_mime_type(mime_type_presentations)

    def sheets_metadata(self, sheet_id):
        return self.execute(self.spreadsheets.get(spreadsheetId=sheet_id))

    def get_values(self, sheet_id, range):
        values = self.spreadsheets.values()
        result = self.execute(values.get(spreadsheetId = sheet_id ,
                                         range         = range    ))
        return result.get('values')

    def set_values(self, sheet_id, range, values):
        value_input_option = 'RAW' # vs USER_ENTERED
        body               = { 'values' : values }
        result = self.execute(self.spreadsheets.values().update( spreadsheetId    = sheet_id,
                                                                 range            = range,
                                                                 valueInputOption = value_input_option,
                                                                 body             = body))
        return result


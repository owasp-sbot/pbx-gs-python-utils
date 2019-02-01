from unittest         import TestCase
from gsuite.GDrive    import GDrive
from gsuite.GSheets   import GSheets
from utils.Dev import Dev
from utils.Misc import Misc


class Test_GDrive(TestCase):
    def setUp(self):
        self.gsheets = GSheets()

    def test_ctor(self):
        spreadsheets = self.gsheets.spreadsheets
        Dev.pprint(spreadsheets)
        #assert spreadsheets._baseUrl == 'https://sheets.googleapis.com/'

    # Helper Methods

    def get_target_slide_id(self):
        file_id  = self.spreadsheets.gdrive.find_by_name('Test sheet').get('id')
        #slides   = self.gslides.slides(self.test_id)
        #slide_id = slides.pop().get('objectId')
        #return file_id, slide_id
        return file_id

    # GSheets methods

    def test_all_spreadsheets(self):
        spreadsheets = self.gsheets.all_spreadsheets()
        assert len(spreadsheets) > 0

    def test_execute_requests(self):
        sheet_id = self.get_target_slide_id()
        # this is one wat to add values via the execute requests workflow
        requests = [{   'updateCells': {
                                        'start': {'sheetId': 0, 'rowIndex': 11, 'columnIndex': 0},
                                        'rows': [
                                            {
                                                'values': [
                                                    {
                                                        'userEnteredValue': {'numberValue': 1},
                                                        'userEnteredFormat': {'backgroundColor': {'red': 1}}
                                                    }, {
                                                        'userEnteredValue': {'numberValue': 2},
                                                        'userEnteredFormat': {'backgroundColor': {'blue': 1}}
                                                    }, {
                                                        'userEnteredValue': {'numberValue': 3},
                                                        'userEnteredFormat': {'backgroundColor': {'green': 1}}
                                                    }
                                                ]
                                            }
                                        ],
                                        'fields': 'userEnteredValue,userEnteredFormat.backgroundColor'
                                    }
                                }]
        result = self.gsheets.execute_requests(sheet_id,requests)
        Dev.pprint(result)

    def test_sheets_metadata(self):
        sheet_id = self.get_target_slide_id()
        metadata = self.gsheets.sheets_metadata(sheet_id)
        sheets = metadata.get('sheets')

        assert sheets[0].get('properties').get('title') == 'Sheet1'

    def test_values(self):
        sheet_id = self.get_target_slide_id()
        range    = "Sheet1!A2:D4"
        values = self.gsheets.get_values(sheet_id, range)
        assert values[0] == ['1 1', '1 2', '1 3']

    def test_set_values(self):
        sheet_id = self.get_target_slide_id()
        range    = "Sheet1!B17:D18"
        values   = [ ["a","b","c"],[1,2,3]]
        result   = self.gsheets.set_values(sheet_id,range,values)
        assert result == {  'spreadsheetId' : '158e_ijqFk8vka1dLQ9WLlinrFr4Rb4yXbIMdAM0C87g',
                            'updatedCells'  : 6,
                            'updatedColumns': 3,
                            'updatedRange'  : 'Sheet1!B17:D18',
                            'updatedRows'   : 2 }
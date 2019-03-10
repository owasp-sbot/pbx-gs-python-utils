from unittest import TestCase

from api_jira.API_JIRA_Sheets_Sync import API_JIRA_Sheets_Sync
from utils.Dev import Dev


class Test_API_JIRA_Sheets_Sync(TestCase):

    def setUp(self):
        self.file_id  = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        self.api_sync = API_JIRA_Sheets_Sync(self.file_id)


    def test_jira__gsheets(self):
        Dev.pprint(self.api_sync.jira())
        Dev.pprint(self.api_sync.gsheets())

    def test_convert_sheet_data_to_raw_data(self):
        sheet_data = self.api_sync.get_sheet_data()
        raw_data = self.api_sync.convert_sheet_data_to_raw_data(sheet_data)
        Dev.pprint(raw_data)

    def test_get_issue_data(self):
        Dev.pprint(self.api_sync.get_issue_data('RISK-1200'))

    def test_get_sheet_data(self):
        result = self.api_sync.get_sheet_data()
        Dev.pprint(result)

    def test_get_sheet_raw_data(self):
        result = self.api_sync.get_sheet_raw_data()
        Dev.pprint(result)

    def test_update_sheet_data_with_jira_data(self):
        sheet_data = self.api_sync.get_sheet_data()
        self.api_sync.update_sheet_data_with_jira_data(sheet_data)
        Dev.pprint(sheet_data)

    def test_update_file_with_raw_data(self):
        sheet_data = self.api_sync.get_sheet_data()
        self.api_sync.update_sheet_data_with_jira_data(sheet_data)
        raw_data   = self.api_sync.convert_sheet_data_to_raw_data(sheet_data)
        self.api_sync.update_file_with_raw_data(raw_data)

    def test_sync_sheet_with_jira(self):
        self.api_sync.sync_sheet_with_jira()


    def test_sync_sheet_with_jira__bad_file_id(self):
        self.api_sync.file_id = 'aaaa'
        Dev.pprint(self.api_sync.sync_sheet_with_jira())





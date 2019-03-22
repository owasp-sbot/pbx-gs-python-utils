from unittest import TestCase

from api_jira.API_Jira_Sheets_Create import API_Jira_Sheets_Create
from utils.Dev import Dev


class Test_API_JIRA_Sheets_Create(TestCase):
    def setUp(self):
        self.file_id = '1eQbkiTexDq_LKGqYRdzs1i4sfYq_2lef8SbtKvFqbtQ'
        self.sheets_create = API_Jira_Sheets_Create(self.file_id)

    # def test_get_sheet_contents(self):
    #     sheet_name = self.sheets_create.sheet_name()
    #     Dev.pprint(self.sheets_create.get_sheet_data(sheet_name))
    #     Dev.pprint(self.sheets_create.headers)

    def test_create_create_jira_tickets_object(self):
        sheet_data   = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        Dev.pprint(jira_actions)

    def test_execute_jira_actions(self):
        sheet_data = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        self.sheets_create.execute_jira_actions(jira_actions)
        self.sheets_create.update_sheet_with_status(jira_actions)

    def test_update_sheet_with_status(self):
        sheet_data   = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        self.sheets_create.update_sheet_with_status(jira_actions)
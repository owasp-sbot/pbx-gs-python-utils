from api_jira.API_Jira import API_Jira, use_local_cache_if_available
from gsuite.GSheets import GSheets
from utils.Dev import Dev


class API_JIRA_Sheets_Sync:
    def __init__(self, sheet_id, sheet_name = None):
        self._gsheets    = None
        self._jira       = None
        self.file_id     = sheet_id
        self._sheet_name = sheet_name
        self.headers     = []

    # Helper methods
    def jira(self):
        if self._jira is None:
            self._jira = API_Jira()
        return self._jira

    def gsheets(self):
        if self._gsheets is None:
            self._gsheets = GSheets()
        return self._gsheets

    def sheet_name(self):
        if self._sheet_name is None:
            self._sheet_name = list(set(self.gsheets().sheets_properties_by_title(self.file_id))).pop(0)
        return self._sheet_name


    # main methods

    def convert_sheet_data_to_raw_data(self,sheet_data):
        raw_data = [self.headers]
        for item in sheet_data:
            row = []
            for header in self.headers:
                row.append(item.get(header))
            raw_data.append(row)
        return raw_data

    def get_sheet_raw_data(self):
        return self.gsheets().get_values(self.file_id, self.sheet_name())

    #@use_local_cache_if_available
    def get_sheet_data(self):
        rows = self.get_sheet_raw_data()
        self.headers = rows.pop(0)
        data = []
        for row_index, row in enumerate(rows):
            item = { 'index':row_index}
            for header_index, header in enumerate(self.headers):
                if header_index >= len(row):
                    value = None
                else:
                    value  = row[header_index].strip()
                item[header] = value
            data.append(item)
        return data

    def update_sheet_data_with_jira_data(self,sheet_data):
        for item in sheet_data:
            issue = self.get_issue_data(item.get('Key'))
            if issue:
                for column_id in set(item):
                    value = issue.get(column_id)
                    if value:
                        item[column_id] = value

    @use_local_cache_if_available
    def get_issue_data(self,issue_id):
        return self.jira().issue(issue_id)

    def update_file_with_raw_data(self,raw_data):
        self.gsheets().set_values(self.file_id, self.sheet_name(), raw_data)

    def sync_sheet_with_jira(self):
        sheet_data = self.get_sheet_data()
        self.update_sheet_data_with_jira_data(sheet_data)
        raw_data = self.convert_sheet_data_to_raw_data(sheet_data)
        self.update_file_with_raw_data(raw_data)
        return "sync done"


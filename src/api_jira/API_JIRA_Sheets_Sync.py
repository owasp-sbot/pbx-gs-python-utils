from api_jira.API_Jira import API_Jira, use_local_cache_if_available, save_result_to_local_cache, Json
from gsuite.GSheets import GSheets
from utils.Dev import Dev


class API_JIRA_Sheets_Sync:
    def __init__(self, file_id,gsuite_secret_id=None):
        self._gsheets         = None
        self._jira            = None
        self.file_id          = file_id
        self._sheet_name      = None
        self._sheet_id        = None
        self.headers          = []
        self.gsuite_secret_id = gsuite_secret_id
        if not self.gsuite_secret_id:
            self.gsuite_secret_id = 'gsuite_gsbot_user'

    # Helper methods
    def jira(self):
        if self._jira is None:
            self._jira = API_Jira()
        return self._jira

    def gsheets(self):
        if self._gsheets is None:
            self._gsheets = GSheets(gsuite_secret_id=self.gsuite_secret_id)
        return self._gsheets

    def sheet_name(self):
        if self._sheet_name is None:
            sheets = self.gsheets().sheets_properties_by_title(self.file_id)
            if sheets:
                self._sheet_name = list(set(sheets)).pop(0)
        return self._sheet_name

    def sheet_id(self):
        if self._sheet_id is None:
            sheets = self.gsheets().sheets_properties_by_id(self.file_id)
            if sheets:
                self._sheet_id = list(set(sheets)).pop(0)
        return self._sheet_id


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

    #@save_result_to_local_cache
    #@use_local_cache_if_available
    def get_sheet_data(self):
        rows = self.get_sheet_raw_data()
        if rows:
            self.headers = rows.pop(0)
            data = []
            for row_index, row in enumerate(rows):
                item = { 'index':row_index}
                for header_index, header in enumerate(self.headers):
                    if header_index >= len(row):
                        value = None
                    else:
                        value  = row[header_index].strip()
                    if header == 'Jira Link' and len(row) > 0:
                        value = '=HYPERLINK("https://jira.photobox.com/browse/{0}","{0}")'.format(row[0])
                    item[header] = value
                data.append(item)
            return data

    def color_code_cells_based_on_diff_status(self, diff_cells):
        sheet_id = self.sheet_id()

        requests = []
        for diff_cell in diff_cells:
            col    = diff_cell.get('col_index')
            row    = diff_cell.get('row_index')
            status = diff_cell.get('status')
            if status == 'diff': requests.append(self.gsheets().request_cell_set_background_color(sheet_id, col ,row, 1   ,0.5 ,0.5))
            if status == 'same': requests.append(self.gsheets().request_cell_set_background_color(sheet_id, col ,row, 0.5 ,1   ,0.5))

        self.gsheets().execute_requests(self.file_id, requests)

    def diff_sheet(self):
        sheet_data  = self.get_sheet_data()
        issues      = self.get_jira_issues_in_sheet_data(sheet_data)
        diff_cells  = self.diff_sheet_data_with_jira_data(sheet_data, issues)
        self.color_code_cells_based_on_diff_status(diff_cells)

    def diff_sheet_data_with_jira_data(self,sheet_data, jira_data):
        diff_cells = []
        print()
        for row_index, row in enumerate(sheet_data):
            for header_index, header in enumerate(self.headers):
                key = row['Key']
                issue = jira_data.get(key)
                if issue:
                    sheet_value = row.get(header)
                    jira_value  = issue.get(header,'')
                    if sheet_value and jira_value:
                        diff_cell = {
                                        'row_index'   : row_index + 1,
                                        'col_index'   : header_index ,
                                        'sheet_value' : sheet_value  ,
                                        'jira_value'  : jira_value
                                    }
                        if sheet_value   == jira_value: diff_cell['status'] = 'same'
                        elif sheet_value != jira_value: diff_cell['status'] = 'diff'
                        #print("{0:10} {1:20} {2:20} {3:20}".format(key, header, sheet_value, jira_value))
                        diff_cells.append(diff_cell)
        return diff_cells

    def update_sheet_data_with_jira_data(self,sheet_data):
        for item in sheet_data:
            issue = self.get_issue_data(item.get('Key'))
            if issue:
                for column_id in set(item):
                    value = issue.get(column_id)
                    if value:
                        item[column_id] = value

    def get_jira_issues_in_sheet_data(self, sheet_data):
        #return Json.load_json('/tmp/tmp_issues.json')
        keys = [row.get('Key') for row in sheet_data if row.get('Key') != '']
        issues = self.jira().issues(keys)
        Json.save_json('/tmp/tmp_issues.json', issues)
        return issues

    #@use_local_cache_if_available
    def get_issue_data(self,issue_id):
        return self.jira().issue(issue_id)

    def update_file_with_raw_data(self,raw_data):
        self.gsheets().set_values(self.file_id, self.sheet_name(), raw_data)

    def sync_sheet_with_jira(self):
        sheet_data = self.get_sheet_data()
        if sheet_data:
            self.update_sheet_data_with_jira_data(sheet_data)
            raw_data = self.convert_sheet_data_to_raw_data(sheet_data)
            self.update_file_with_raw_data(raw_data)
            return "sync done .... "
        return "Error: no data for file_id: {0}".format(self.file_id)
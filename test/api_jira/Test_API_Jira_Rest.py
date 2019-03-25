from unittest import TestCase

from api_jira.API_Jira_Rest import API_Jira_Rest
from utils.Dev import Dev


class Test_API_Jira_Rest(TestCase):

    def setUp(self):
        self.api = API_Jira_Rest()

    def test_config(self):
        Dev.print(self.api.config())

    def test_fields(self):
        for field in self.api.fields():
            print(field.get('id'), field.get('name'))

    def test_fields_by_id(self):
        Dev.pprint(self.api.fields_by_id())

    def test_fields_by_name(self):
        Dev.pprint(self.api.fields_by_name())

    def test_fields_by_name__performance_test(self):        # test what happens when this method is called multiple times
        for i in range(0,2):
            Dev.pprint(len(self.api.fields_by_name()))

    def test_issue_raw(self):
        issue_id= 'RISK-12'
        result = self.api.issue(issue_id)
        assert set(result) == {'key', 'fields', 'expand', 'id', 'self'}
        Dev.pprint(result)

    def test_issue(self):
        issue_id = 'RISK-12'
        issue_id = 'SL-118'
        issue_id = 'RISK-1573'
        result = self.api.issue(issue_id)
        Dev.pprint(result)

    def test_issues(self):
        issues_ids = ['RISK-12','RISK-424','SL-118','IA-12']
        result = self.api.issues(issues_ids)
        Dev.pprint(result)

    def test_issue_update_field(self):
        issue_id = 'RISK-12'
        summary = 'updated via a rest put request.'
        result = self.api.issue_update_field(issue_id, 'summary', summary)
        Dev.pprint(result)

    def test_issue_update_fields(self):
        issue_id = 'RISK-12'
        fields = {  "Summary"         : "update from test... 12345"  ,
                    "Description"     : "The description.....123456"     ,
                    "Risk Description": "The risk description"     ,
                    "Labels"          : "Risk,Unit-Test"           ,
                    #"Priority"        : "Major"                    ,
                    "Risk Rating"     : "Low"                     ,
                    "Assignee"        : "james.wharton"               }
        result = self.api.issue_update_fields(issue_id, fields)
        Dev.pprint(result)

    def test_issue_update_field___status(self):             # for this to work I believe we need to a) send a transition id , and b) make sure they are one of the ones allowed next

        issue_id    = 'RISK-12'                             # see method issue_transition_to

        # from api_jira.API_Jira import API_Jira
        # jira = API_Jira()
        # result = jira.issue(issue_id)
        # result = jira.issue_next_transitions(issue_id)
        # Dev.pprint(result)

        #return

        issue_start = self.api.issue(issue_id)
        Dev.pprint(issue_id)
        #status = issue_start.get('Status')
        fields = { 'transition' : 12348 }
        result = self.api.issue_update_fields(issue_id, fields)
        Dev.pprint(result)

    def test_issue_status_available(self):
        issue_id = 'RISK-12'
        result = self.api.issue_status_available(issue_id)
        Dev.pprint(result)


    #def test_issue_update_field___assignee(self):          # this one is working
    #def test_issue_update_field___dates(self):             # do this one next
        

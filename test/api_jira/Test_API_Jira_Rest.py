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

    def test_issue(self):
        issue_id= 'RISK-12'
        result = self.api.issue(issue_id)
        Dev.pprint(result)

    def test_issue_update_field(self):
        issue_id = 'RISK-12'
        summary = 'updated via a rest put request.'
        result = self.api.issue_update_field(issue_id, 'summary', summary)
        Dev.pprint(result)

    def test_issue_update_fields(self):
        issue_id = 'RISK-12'
        fields = {  "Summary"         : "update from test... 12345"  ,
                    "Description"     : "The description.....123"     ,
                    "Risk Description": "The risk description"     ,
                    "Labels"          : "Risk,Unit-Test,ABC"           ,
                    #"Priority"        : "Major"                    ,
                    "Risk Rating"     : "Low"                     ,
                    "Assignee"        : "dinis.cruz"               }
        result = self.api.issue_update_fields(issue_id, fields)
        Dev.pprint(result)
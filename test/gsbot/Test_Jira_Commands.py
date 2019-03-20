from unittest import TestCase
from gs_jira.Jira_Commands import Jira_Commands
from utils.Dev import Dev


class Test_Jira_Commands(TestCase):

    def setUp(self):
        self.api = Jira_Commands()

    def test_projects(self):
        result = self.api.projects()
        Dev.pprint(result)

    def test_issue(self):
        Dev.pprint(self.api.issue(params=['AAA-12' ]))
        Dev.pprint(self.api.issue(params=['RISK-12']))

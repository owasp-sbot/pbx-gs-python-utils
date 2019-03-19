from unittest import TestCase
from gsbot.Jira_Commands import Jira_Commands
from utils.Dev import Dev


class Test_Jira_Commands(TestCase):

    def setUp(self):
        self.jira_sync = Jira_Commands()

    def test_projects(self):
        result = self.jira_sync.projects()
        Dev.pprint(result)

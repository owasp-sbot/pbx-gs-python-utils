from unittest import TestCase

from gs_jira.GS_Bot_Jira_Commands import GS_Bot_Jira_Commands
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_GS_Bot_Jira_Commands(TestCase):

    def setUp(self):
        self.jira_commands = GS_Bot_Jira_Commands()

    def test_invoke(self):
        result = GS_Bot_Jira_Commands.invoke()
        Dev.pprint(result)


    def test_update_lambda(self):
        Lambdas('gsbot.gsbot_gs_jira').update_with_src()
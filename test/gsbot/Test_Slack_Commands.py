from unittest import TestCase

from gsbot.Slack_Commands import Slack_Commands
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Test_Slack_Commands(TestCase):
    def setUp(self):
        self.slack = Slack_Commands()

    def test_username_to_id(self):
        result = self.slack.username_to_id()
        Dev.pprint(result)

    def test_stats(self):
        result = self.slack.stats(team_id='T0SDK1RA8')
        Dev.pprint(result)

    def test_user_info(self):
        result = self.slack.user_info(params=['gsbot'])
        Dev.pprint(result)
        assert self.slack.user_info(params=['aaaaa']) == ':exclamation: Sorry, could not find user with alias `aaaaa`'

    def test_user_info__by_Id(self):
        result = self.slack.user_info(params=['U7ESE1XS7'])
        Dev.pprint(result)


    def test__update_lambda(self):
        Lambdas('gsbot.gsbot_slack').update()




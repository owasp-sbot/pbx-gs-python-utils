import unittest
from   utils.Dev        import *
from utils.aws.Lambdas import Lambdas


class Test_Lambda_gsbot_gs_jira(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambdas('gsbot.gsbot_gs_jira', memory = 3008)

    def test_lambda_update(self):
        self.step_lambda.update_with_src()


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {'team_id':'T7F3AUXGV', 'channel':'DDKUZTK6X'}}
        return self.step_lambda.upload_and_invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_invoke(self):
        response = self._send_command_message('invoke')
        Dev.pprint(response)

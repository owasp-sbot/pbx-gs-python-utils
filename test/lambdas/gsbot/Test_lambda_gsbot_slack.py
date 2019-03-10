import unittest
from   utils.Dev        import *
from utils.aws.Lambdas import Lambdas


class Test_Lambda_gs_bot(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambdas('gsbot.gsbot_slack', memory = 3008)

    def test_lambda_update(self):
        self.step_lambda.update_with_src()


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {}}
        return self.step_lambda.upload_and_invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_hello(self):
        response = self._send_command_message('test')
        Dev.pprint(response)

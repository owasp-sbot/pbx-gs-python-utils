import  unittest

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.lambdas.gsbot.gsbot_slack import run


class test_lambda_gs_bot(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambda('pbx_gs_python_utils.lambdas.gsbot.gsbot_slack')

    #def test_lambda_update(self):
    #    self.step_lambda.update_with_src()

    def test_invoke_directly(self):
        payload = {'params': [], 'data': {}}
        text,attachments = run(payload,{})
        assert text == '*Here are the `Slack_Commands` commands available:*'


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {}}
        return self.step_lambda.invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_bad_command(self):
        response = self._send_command_message('test')
        assert response == [ ':red_circle: command not found `test`\n'
                              '\n'
                              '*Here are the `Slack_Commands` commands available:*',
                              [ { 'actions': [],
                                  'callback_id': '',
                                  'color': 'good',
                                  'fallback': None,
                                  'text': ' • stats\n • user_info\n • username_to_id\n'}]]



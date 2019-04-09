from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from osbot_aws.apis.Lambda           import Lambda


class Test_Lambdas_Helpers(TestCase):

    def test_slack_message(self):
        result = slack_message('an message')
        Dev.pprint(result)

    def test_slack_message_to_org(self):
        def send_message(team_id, channel):

            text = 'direct slack message to team_id: {0}'.format(team_id)
            attachments  = []


            payload = {
                            'text': text,
                            'attachments': attachments,
                            'channel': channel,
                            'team_id': team_id
                        }

            result = Lambda('pbx_gs_python_utils.lambdas.utils.slack_message').invoke(payload)
            assert result.get('ok'     ) == True
            assert result.get('channel') == channel

        send_message('T0SDK1RA8', 'DG30MH0KV')
        send_message('T7F3AUXGV', 'GDL2EC3EE')
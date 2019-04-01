from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Test_Lambdas_Helpers(TestCase):

    def test_slack_message(self):
        result = slack_message('an message')
        Dev.pprint(result)

    def test_slack_message_to_pbx_org(self):
        text = 'an test'
        attachments  = []
        team_id = 'T0SDK1RA8'
        channel = 'DG30MH0KV'

        team_id = 'T7F3AUXGV'
        channel = 'GDL2EC3EE'

        payload = {
                        'text': text,
                        'attachments': attachments,
                        'channel': channel,
                        'team_id': team_id
                    }

        result = Lambdas('pbx_gs_python_utils.lambdas.utils.slack_message').invoke(payload)
        #result = slack_message('an message', channel=channel, team_id=team_id)
        Dev.pprint(result)

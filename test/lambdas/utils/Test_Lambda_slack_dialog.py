import  unittest
from    utils.Dev              import Dev
from osbot_aws.apis.Lambda           import Lambda


class Test_Lambda_slack_message(unittest.TestCase):
    def setUp(self):
        self.slack_dialog = Lambda('utils.slack_dialog', path_libs = '../_lambda_dependencies/slack')

    def test_update(self):
        Dev.pprint(self.slack_dialog.update().invoke())  # this lambda is really hard to test since we need a valid trigger_id from Slack (which only lasts 3 secs
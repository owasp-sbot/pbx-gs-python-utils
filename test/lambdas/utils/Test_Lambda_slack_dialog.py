import base64
import os
import tempfile

import  pydot
import  unittest
from    utils.Dev              import Dev
from    utils.Show_Img import Show_Img
from    utils.aws.Lambdas      import Lambdas


class Test_Lambda_slack_message(unittest.TestCase):
    def setUp(self):
        self.slack_dialog = Lambdas('utils.slack_dialog', path_libs = '../_lambda_dependencies/slack')

    def test_update(self):
        Dev.pprint(self.slack_dialog.update().invoke())  # this lambda is really hard to test since we need a valid trigger_id from Slack (which only lasts 3 secs
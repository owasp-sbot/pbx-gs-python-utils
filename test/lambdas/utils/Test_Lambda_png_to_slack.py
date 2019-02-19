import base64
import unittest

from gsuite.GDrive import GDrive
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Lambda_pdf_to_slack(unittest.TestCase):
    def setUp(self):
        self.png_to_slack = Lambdas('utils.png_to_slack', memory=3008)

    def test_update_and_invoke(self):
        png_file = '/tmp/lambda_png_file.png'
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode()
        Dev.pprint(png_data)
        payload   = { "png_data": png_data, 'aws_secrets_id':'slack-gs-bot', 'channel': 'DDKUZTK6X'}

        result = self.png_to_slack.update_with_src().invoke(payload)

        Dev.pprint(result)
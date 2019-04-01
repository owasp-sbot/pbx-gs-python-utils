import base64
import unittest

from gsuite.GDrive import GDrive
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas
from pbx_gs_python_utils.utils.aws.s3 import S3


class Test_Lambda_pdf_to_slack(unittest.TestCase):
    def setUp(self):
        self.png_to_slack = Lambdas('utils.png_to_slack', memory=3008)

    def test_update_and_invoke(self):
        png_file = '/tmp/lambda_png_file.png'
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode()
        Dev.pprint(len(png_data))
        payload   = { "png_data": png_data, 'aws_secrets_id':'slack-gs-bot', 'channel': 'DDKUZTK6X'}

        result = self.png_to_slack.update_with_src().invoke(payload)

        Dev.pprint(result)

    def test__delete_temp_png_files(self):
        s3_bucket = 'gs-lambda-tests'

        tmp_files = S3().find_files(s3_bucket, S3().tmp_file_folder)
        for tmp_file in tmp_files:
            S3().file_delete(s3_bucket, tmp_file)

        Dev.pprint(S3().find_files(s3_bucket, S3().tmp_file_folder))


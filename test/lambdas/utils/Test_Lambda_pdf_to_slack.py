import base64
import unittest

from gsuite.GDrive import GDrive
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Lambda_pdf_to_slack(unittest.TestCase):
    def setUp(self):
        self.pdf_to_slack = Lambda('utils.pdf_to_slack', memory=3008).create()
        #Lambda('utils.puml_to_png', memory=3008).delete().create()

    def test_update_and_invoke(self):

        gdrive    = GDrive()
        file_id   = gdrive.find_by_name('GSlides API tests').get('id')
        pdf_bytes = gdrive.file_export(file_id)
        pdf_data  = base64.b64encode(pdf_bytes).decode()
        payload   = { "pdf_data": pdf_data, 'channel': 'DDKUZTK6X'}

        result = self.pdf_to_slack.update_with_src().invoke(payload)

        Dev.pprint(result)
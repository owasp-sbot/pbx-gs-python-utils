import base64
import unittest

from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Lambda_lambda_browser(unittest.TestCase):
    def setUp(self):
        self.lambda_browser = Lambdas('browser.lambda_browser',memory=3008).create()


    def test_update_and_invoke(self):
        payload ={ "params" : []}
        result = self.lambda_browser.update_with_src().invoke(payload)
        Dev.pprint(result)

    def test_screenshot_url(self):
        url = 'https://www.google.co.uk'
        url = 'http://visjs.org/'
        payload = {"params": ['screenshot_url',url]}
        result = self.lambda_browser.update_with_src().invoke(payload)


        Dev.pprint(result)
        
        png_data = result.get('body')
        png_file = '/tmp/lambda_png_file.png'
        if png_data:
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(png_data.encode()))

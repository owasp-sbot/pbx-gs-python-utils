import base64
import os
from unittest import TestCase

from browser.Browser_Commands import Browser_Commands
from utils.Dev import Dev


class Test_Browser_Commands(TestCase):

    def setUp(self):
        self.browser_commands = Browser_Commands()

    def _save_png_data(self, png_data):
        png_file = '/tmp/lambda_png_file.png'
        if png_data:
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(png_data.encode()))

    def test_list(self):
        result = self.browser_commands.list(None, None, None)
        Dev.pprint(result)

    def test_screenshot(self):
        os.environ['OSX_CHROME'] = 'True'
        team_id = 'T7F3AUXGV'
        channel = 'DDKUZTK6X'
        url = 'https://www.google.co.uk/aaa'
        self.browser_commands.screenshot(team_id, channel, [url])

    def test_render_file(self):
        os.environ['OSX_CHROME'] = 'True'
        result = self.browser_commands.render_file(None,None,None)
        Dev.pprint(result)

    def test_markdown___no_params(self):
        result = self.browser_commands.markdown(None,None,None)
        self._save_png_data(result)
        #Dev.pprint(result)

    def test_markdown___with_params(self):
        params = ["# running from unit test \n","2nd paragraph..."]
        result = self.browser_commands.markdown(None,None,params)
        self._save_png_data(result)
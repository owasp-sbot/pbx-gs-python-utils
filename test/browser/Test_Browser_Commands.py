import os
from unittest import TestCase

from browser.Browser_Commands import Browser_Commands
from utils.Dev import Dev


class Test_Browser_Commands(TestCase):

    def setUp(self):
        self.browser_commands = Browser_Commands()

    def test_screenshot(self):
        os.environ['OSX_CHROME'] = 'True'
        team_id = 'T7F3AUXGV'
        channel = 'DDKUZTK6X'
        url = 'https://www.google.co.uk/aaa'
        self.browser_commands.screenshot(team_id, channel, [url])

    def test(self):
        os.environ['OSX_CHROME'] = 'True'
        result = self.browser_commands.render_file(None,None,None)
        Dev.pprint(result)
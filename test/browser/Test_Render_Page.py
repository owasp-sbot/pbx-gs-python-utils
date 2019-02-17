from unittest import TestCase

from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Misc import Misc


class Test_Render_Page(TestCase):
    def setUp(self):
        self.render_page = Render_Page(headless = False, auto_close = False)

    def test_render_html(self):
        random_value = Misc.random_string_and_numbers(6,"dynamic text ")
        html         = "<html><script>document.write('{0}')</script></html>".format(random_value)
        result = self.render_page.render_html(html)
        assert result('body').html() == random_value


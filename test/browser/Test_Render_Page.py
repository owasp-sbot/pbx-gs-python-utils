from unittest import TestCase

from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc
from utils.Temp_File import Temp_File


class Test_Render_Page(TestCase):
    def setUp(self):
        self.render_page  = Render_Page(headless = False, auto_close = False)
        self.random_value = Misc.random_string_and_numbers(6, "dynamic text ")
        self.html         = "<html><script>document.write('{0}')</script></html>".format(self.random_value)

    def test_render_file(self):
        with Temp_File(self.html, 'html') as temp_file:
            result = self.render_page.render_file(temp_file.file_path)
            assert result('body').html() == self.random_value

    def test_render_html(self):
        result = self.render_page.render_html(self.html)
        assert result('body').html() == self.random_value



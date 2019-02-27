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

    def test_render_folder(self):
        result = self.render_page.render_folder(Files.current_folder())
        Dev.print(result.html())

    def test_render_html(self):
        result = self.render_page.render_html(self.html)
        assert result('body').html() == self.random_value

    def test_screenshot_html(self):
        tmp_img = '/tmp/test_screenshot_html.png'
        img_file = self.render_page.screenshot_html(self.html,tmp_img)
        assert Files.exists(img_file)

    def test_screensh1ot_file(self):
        with Temp_File(self.html, 'html') as temp_file:
            tmp_img = '/tmp/test_screenshot_html.png'
            clip = {'x': 1, 'y': 1, 'width': 180, 'height': 30}
            img_file = self.render_page.screenshot_file(temp_file.file_path,tmp_img,clip=clip)
            assert Files.exists(img_file)

    def test_screenshot_folder(self):
        web_root = Files.current_folder()
        tmp_img  = '/tmp/test_screenshot_html.png'
        clip = {'x': 1, 'y': 1, 'width':280, 'height': 200}
        self.render_page.screenshot_folder(web_root, tmp_img,clip)

    def test_screenshot_file_in_folder(self):
        web_root = Files.current_folder()
        tmp_img = '/tmp/test_screenshot_html.png'
        html_file = 'aaaa.html'
        self.render_page.screenshot_file_in_folder(web_root, html_file, tmp_img)

    def test_screenshot_url(self):
        #url = 'https://github.com/GoogleChrome/puppeteer'
        #url = 'https://www.google.co.uk'
        #url = 'http://visjs.org/examples/network/other/manipulation.html'
        #url = 'http://visjs.org/examples/graph3d/01_basics.html'
        url = 'https://getbootstrap.com/docs/4.3/examples/dashboard/'
        tmp_img = '/tmp/test_screenshot_html.png'
        self.render_page.screenshot_url(url, tmp_img)



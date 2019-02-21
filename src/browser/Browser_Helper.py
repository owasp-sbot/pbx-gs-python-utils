import os

from utils.Files import Files
from utils.aws.Lambdas import load_dependency


class Browser_Helper:
    def __init__(self):
        self.api_browser = None
        self.render_page = None

    def open_local_page_and_get_screenshot(self, path, js_code):
        with self.render_page.web_server as web_server:
           url      = web_server.url(path)
           return self.render_page.get_screenshot_via_browser(url, js_code=js_code)

    def setup(self):

        if os.getenv('AWS_REGION'):
            self.setup_AWS()
        else:
            self.setup_local()

        from browser.API_Browser import API_Browser
        from browser.Render_Page import Render_Page
        self.api_browser = API_Browser().sync__setup_browser()
        self.render_page = Render_Page(api_browser=self.api_browser, web_root=self.web_root())

        return self

    def setup_AWS(self):
        load_dependency('syncer')
        load_dependency('requests')

    def setup_local(self):
        return

    def web_root(self):
        if os.getenv('AWS_REGION') is not None:         # if we are in AWS
            return Files.path_combine('.','./web_root')
        if 'test/browser' in Files.current_folder():    # if we are in an unit test
            return  Files.path_combine('.','../../../../src/web_root')
        return None

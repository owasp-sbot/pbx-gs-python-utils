from syncer import sync

from browser.API_Browser import API_Browser
from browser.Web_Server import Web_Server
from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc


class Render_Page:

    def __init__(self, headless = True, auto_close = True):
        self.web_server = Web_Server()
        self.api_browser = API_Browser(headless,auto_close)


    def render_html(self, html):
        tmp_file  = Misc.random_filename('.html')
        file_path = self.web_server.path_to_file(tmp_file)
        file_url  = self.web_server.url(tmp_file)
        Files.write(file_path, html)
        self.web_server.start()
        result = self.get_page_html_via_browser(file_url)
        self.web_server.stop()
        Files.delete(file_path)
        return result

    @sync
    async def get_page_html_via_browser(self, url):
        await self.api_browser.browser()
        await self.api_browser.open(url)
        return await self.api_browser.html()


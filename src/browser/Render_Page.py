from syncer import sync

from browser.API_Browser import API_Browser
from browser.Web_Server import Web_Server, Web_Server_Temp_File
from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc


class Render_Page:

    def __init__(self, headless = True, auto_close = True):
        self.web_server = Web_Server()
        self.api_browser = API_Browser(headless,auto_close)

    def render_file(self, file_path):
        return self.render_html(Files.contents(file_path))

    def render_html(self, html):
        temp_file = Web_Server_Temp_File(self.web_server,html)
        with self.web_server:
            with temp_file:
                result = self.get_page_html_via_browser(temp_file.url())
        return result

    @sync
    async def get_page_html_via_browser(self, url):
        await self.api_browser.browser()
        await self.api_browser.open(url)
        return await self.api_browser.html()


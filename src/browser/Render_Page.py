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

    def render_file(self, html_file):
        return self.render_html(Files.contents(html_file))

    def render_html(self, html):
        temp_file = Web_Server_Temp_File(self.web_server,html)
        with self.web_server:
            with temp_file:
                result = self.get_page_html_via_browser(temp_file.url())
        return result

    def screenshot_html(self,html,img_file=None, clip=None):
        with self.web_server:
            with Web_Server_Temp_File(self.web_server,html) as temp_file:
                return self.get_screenshot_via_browser(temp_file.url(), img_file,clip=clip)

    def screenshot_file(self,html_file,img_file=None, clip=None):
        return self.screenshot_html(Files.contents(html_file),img_file, clip)

    def screenshot_url(self, url, img_file, clip=None):
        return self.get_screenshot_via_browser(url, img_file, clip=clip)


    @sync
    async def get_page_html_via_browser(self, url):
        await self.api_browser.browser()
        await self.api_browser.open(url)
        return await self.api_browser.html()

    @sync
    async def get_screenshot_via_browser(self, url, target_file=None,full_page=True, clip=None,viewport=None    ):
        if clip        is not None: full_page    = False
        if target_file is None    : target_file = Files.temp_file('.png')
        await self.api_browser.browser()
        #await self.api_browser.open(url)
        #viewport = { 'width': 5000, 'height': 4000}
        #full_page = False
        return await self.api_browser.screenshot(url,full_page=full_page,file_screenshot=target_file, clip=clip, viewport=viewport)


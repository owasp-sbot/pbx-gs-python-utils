from syncer import sync

from browser.API_Browser import API_Browser
from browser.Web_Server import Web_Server, Web_Server_Temp_File
from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc


class Render_Page:

    def __init__(self, api_browser=None, headless = True, auto_close = True, web_root=None, web_server=None):
        if web_server:
            self.web_server = web_server
        else:
            self.web_server = Web_Server(web_root)
        if api_browser:
            self.api_browser = api_browser
        else:
            self.api_browser = API_Browser(headless,auto_close)

    def render_file(self, html_file):
        return self.render_html(Files.contents(html_file))

    def render_folder(self, web_root):
        with self.web_server.set_web_root(web_root):
            return self.get_page_html_via_browser(self.web_server.url())

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

    def screenshot_folder(self,web_root, png_file=None, clip=None):
        with self.web_server.set_web_root(web_root):
            return self.get_screenshot_via_browser(png_file=png_file, clip=clip)

    def screenshot_file_in_folder(self, web_root, html_file, png_file=None, clip=None):
        with self.web_server.set_web_root(web_root):
            url = self.web_server.url(html_file)
            return self.get_screenshot_via_browser(url=url,png_file=png_file, clip=clip)

    def screenshot_url(self, url, img_file, clip=None):
        return self.get_screenshot_via_browser(url, img_file, clip=clip)

    # Sync Helper method (to allow calls to the Async methods to feel like Sync calls)

    @sync
    async def get_page_html_via_browser(self, url,js_code=None):
        await self.api_browser.browser()                # make sure browser is connected
        await self.api_browser.open(url)                # open url
        await self.api_browser.js_execute(js_code)      # execute Javascript
        #return await self.api_browser.html()            # return Html (localy via PyQuery)

    @sync
    async def get_screenshot_via_browser(self, url = None, png_file=None,full_page=True, clip=None,viewport=None, js_code=None,delay=None):
        if clip        is not None: full_page = False
        if png_file    is None    : png_file  = Files.temp_file('.png')
        if url         is None    : url       = self.web_server.url()
        await self.api_browser.browser()
        return await self.api_browser.screenshot(url,full_page=full_page,file_screenshot=png_file, clip=clip, viewport=viewport,js_code=js_code, delay=delay)

    def open_file_in_browser(self, path, js_code=None):
        with self.web_server as web_server:
            url = web_server.url(path)
            return self.get_page_html_via_browser(url,js_code)
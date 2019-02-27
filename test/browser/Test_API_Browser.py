import base64

from syncer import sync
from unittest import TestCase

from browser.API_Browser import API_Browser
from utils.Dev import Dev
from utils.Files import Files
from utils.Http import WS_is_open


class Test_API_Browser(TestCase):

    def setUp(self):
         self.api = API_Browser(headless = False, auto_close = False)

    @sync
    async def test_browser_connect(self):
        browser = await self.api.browser_connect()
        assert WS_is_open(browser.wsEndpoint)

    def test_get_set_last_chrome_session(self):
        self.api.file_tmp_last_chrome_session = Files.temp_file()
        data = { 'chrome_devtools':'ws://127.0.0.1:64979/devtools/browser/75fbaab9-33eb-41ee-afd9-4aed65166791'}
        self.api.set_last_chrome_session(data)
        assert self.api.get_last_chrome_session() == data
        Files.delete(self.api.file_tmp_last_chrome_session)

    @sync
    async def test_js_eval(self):
        markdown = """
# some title "with double quotes"
some text  and 'single quotes'
"""
        encoded_text = base64.b64encode(markdown.encode()).decode()
        js_script = "convert(atob('{0}'))".format(encoded_text)

        result = await self.api.js_eval(js_script)
        Dev.pprint(result)

    @sync
    async def test_invoke_js_function(self):
        markdown = """
# changed title "via js function"
some text  and 'single quotes'
"""
        result = await self.api.js_invoke_function('convert',markdown)
        Dev.pprint(result)

    @sync
    async def test_html(self):
        await self.api.open('https://www.google.com')
        content = await self.api.html()
        assert len(content.html()) > 100

    @sync
    async def test_open(self):
        (headers, status, url, browser) = await self.api.open('https://www.google.com')
        assert headers['x-frame-options'] == 'SAMEORIGIN'
        assert status                     == 200
        assert url                        == 'https://www.google.com/'

    @sync
    async def test_page(self):
        page = await self.api.page()
        assert "http" in page.url


    @sync
    async def test_screenshot(self):
        await self.api.open('https://news.bbc.co.uk')
        file = await self.api.screenshot()
        assert Files.exists(file)


class Test_API_Browser___with_browser_not_closing(TestCase):

    def setUp(self):
        self.api = API_Browser(headless=False, auto_close=False)

    @sync
    async def test_html(self):
        await self.api.open('https://www.google.co.uk')
        content = await self.api.html()
        print(content)
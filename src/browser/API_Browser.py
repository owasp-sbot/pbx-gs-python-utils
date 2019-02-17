from pyppeteer import connect, launch

from utils.Files import Files
from utils.Http import WS_is_open
from utils.Json import Json
from pyquery    import PyQuery


class API_Browser:

    def __init__(self, headless = True, auto_close = True, url_chrome = None):
        self.file_tmp_last_chrome_session = '/tmp/browser-last_chrome_session.json'
        self.file_tmp_screenshot          = '/tmp/browser-page-screenshot.png'
        self._browser                     = None
        self.headless                     = headless
        self.auto_close                   = auto_close
        self.url_chrome                   = url_chrome

    async def browser(self):
        if self._browser is None:
            self._browser = await self.browser_connect()
        return self._browser

    async def browser_connect(self):
        if not self.url_chrome:
            url_chrome = self.get_last_chrome_session().get('url_chrome')
        if url_chrome and WS_is_open(url_chrome):
            self._browser = await connect({'browserWSEndpoint': url_chrome})
        else:
            self._browser = await launch(headless=self.headless, autoClose = self.auto_close)
            self.set_last_chrome_session({'url_chrome': self._browser.wsEndpoint})
        return self._browser

    async def browser_close(self):
        browser = await self.browser()
        if browser is not None:
            await browser.close()

    async def js_eval(self, code):
        page = await self.page()
        return await page.evaluate(code)

    # async def js_invoke(self, method, *args):
    #     page = await self.page()
    #     jscode = "{0}({1})"
    #     return await page.evaluate(method, *args)


    async def open(self, url):
        page      = await self.page()
        response  = await page.goto(url)  # returns response object
        headers   = response.headers
        status    = response.status
        url       = response.url
        return headers, status, url, self

    async def page(self):
        browser = await self.browser()
        pages = await browser.pages()
        return pages.pop()

    async def sleep(self, mseconds):
        page = await self.page()
        await page.waitFor(mseconds);
        return self

    async def html(self):
        page = await self.page()
        content = await page.content()
        return PyQuery(content)

    async def screenshot(self, url= None, full_page = True, file_screenshot = None):
        if url:
            await self.open(url)
        if file_screenshot is None:
            file_screenshot = self.file_tmp_screenshot

        page = await self.page()
        await page.screenshot({'path': file_screenshot, 'fullPage': full_page})
        return file_screenshot


    async def url(self):
        page = await self.page()
        return page.url



    # helper sync functions

    def get_last_chrome_session(self):
        if Files.exists(self.file_tmp_last_chrome_session):
            return Json.load_json(self.file_tmp_last_chrome_session)
        return {}

    def set_last_chrome_session(self, data):
        Json.save_json_pretty(self.file_tmp_last_chrome_session, data)
        return self
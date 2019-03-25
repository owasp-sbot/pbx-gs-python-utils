import base64
import json
import os
from time import sleep

from syncer import sync

from utils.Dev import Dev
from utils.Files import Files
from utils.Http  import WS_is_open
from utils.Json import Json
from utils.Process import Process
from utils.aws.Lambdas import load_dependency


class API_Browser:

    def __init__(self, headless = True, auto_close = True, url_chrome = None):
        self.file_tmp_last_chrome_session = '/tmp/browser-last_chrome_session.json'
        #self.file_tmp_screenshot          = '/tmp/browser-page-screenshot.png'
        self.file_tmp_screenshot          = Files.temp_file('.png')
        self._browser                     = None
        self.headless                     = headless
        self.auto_close                   = auto_close      # happens after taking a screenshot
        self.url_chrome                   = url_chrome
        self.log_js_errors_to_console     = True

    async def browser(self):
        if self._browser is None:
            self._browser = await self.browser_connect()
        return self._browser

    async def browser_connect(self):
        from pyppeteer import connect, launch                               # we can only import this here or we will have a conflict with the AWS headless version
        if not self.url_chrome:
            url_chrome = self.get_last_chrome_session().get('url_chrome')
        if url_chrome and WS_is_open(url_chrome):
            self._browser = await connect({'browserWSEndpoint': url_chrome})
        else:
            self._browser = await launch(headless=self.headless, autoClose = self.auto_close)
            self.set_last_chrome_session({'url_chrome': self._browser.wsEndpoint})
        return self._browser

    async def browser_close(self):          # bug: this is not working 100% since there are still tons of "headless_shell <defunct>" proccess left (one per execution)
        browser = await self.browser()
        if browser is not None:
            pages = await browser.pages()
            for page in pages:              # not sure if this makes any difference
               await page.close()
            await browser.close()

    async def js_execute(self, js_code):
        if js_code:
            if type(js_code).__name__ == 'str':                             # if it is a string, execute it
                return await self.js_eval(js_code)

            if type(js_code).__name__ == 'list':                            # if it is an list (i.e. array)
                list_types = [type(item).__name__ for item in js_code]      # get all array items type
                all_string = list(set(list_types)) == ['str']               # get unique list and check if all are string
                if all_string:                                              # if they are
                    js_code = ";\n".join(js_code)                           # join them all (separated by ;)
                    return await self.js_eval(js_code)                      # execute it

            name   = js_code.get('name')                                    # if js_code was an object
            params = js_code.get('params'  )                                # get the name and params values
            if name and params:
                return await self.js_invoke_function(name, params)          # execute them as a js method

            #from time import sleep                                         # we might need to add some kind of timeout or callback (to handle cases when actions need a bit more time to stabilize after the js execution)
            #sleep(0.250)                                                   # but I think this is better done outside this function

    async def js_eval(self, code):
        page = await self.page()
        try:
            return await page.evaluate(code)
        except Exception as error:
            error_message = "[js eval error]: {0}".format(error)
            if self.log_js_errors_to_console:
                print(error_message)
            return error_message

    async def js_invoke_function(self, name, params=None):
        if params:
            if type(params).__name__ != 'str':
                params = json.dumps(params)
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0}(JSON.parse(atob('{1}')))".format(name, encoded_text )
            else:
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0}(atob('{1}'))".format(name, encoded_text)
        else:
            js_script = "{0}()".format(name)
        return await self.js_eval(js_script)

    async def js_assign_variable(self, variable, data=None):
        if data:
            if type(data).__name__ != 'str':
                params = json.dumps(data)
                encoded_text = base64.b64encode(params.encode()).decode()
                js_script = "{0} = JSON.parse(atob('{1}'))".format(variable, encoded_text )
            else:
                encoded_text = base64.b64encode(data.encode()).decode()
                js_script = "{0} = atob('{1}')".format(variable, encoded_text)
        else:
            js_script = "{0} = undefined".format(variable)
        return await self.js_eval(js_script)


    # async def js_invoke(self, method, *args):
    #     page = await self.page()
    #     jscode = "{0}({1})"
    #     return await page.evaluate(method, *args)


    async def open(self, url, wait_until=None):
        page      = await self.page()
        if wait_until:
            response  = await page.goto(url, waitUntil= wait_until)  # returns response object
        else:
            response = await page.goto(url)

        if response:
            headers   = response.headers
            status    = response.status
            url       = response.url
            return headers, status, url, self
        return None, None, url, self

    async def page(self):
        browser = await self.browser()
        pages = await browser.pages()
        return pages.pop()

    async def sleep(self, mseconds):
        page = await self.page()
        await page.waitFor(mseconds);
        return self

    async def html(self):
        try:
            from pyquery import PyQuery         # add it here since there was some import issues with running it in lambda (etree). Also this method should not be that useful inside an lambda
            content = await self.html_raw()
            return PyQuery(content)
        except:
            return await self.html_raw()

    async def html_raw(self):
        page = await self.page()
        return await page.content()

    async def screenshot(self, url= None, full_page = True, file_screenshot = None, clip=None, viewport=None, js_code=None, delay=None):
        if url:
            await self.open(url)

        await self.js_execute(js_code)

        if delay:
            sleep(delay)

        if file_screenshot is None:
            file_screenshot = self.file_tmp_screenshot

        page = await self.page()
        if viewport:
            await self.viewport(viewport)
        if clip:
            full_page = False
        await page.screenshot({'path': file_screenshot,'fullPage': full_page, 'clip' : clip})
        if self.auto_close:
            await self.browser_close()
        return file_screenshot


    async def url(self):
        page = await self.page()
        return page.url

    async def page_size(self, width, height):
        page = await self.page()
        await page.setViewport({'width': width, 'height': height})
        return self

    async def viewport(self, viewport):
        page = await self.page()
        await page.setViewport(viewport)
        return self

    def get_last_chrome_session(self):
        if Files.exists(self.file_tmp_last_chrome_session):
            return Json.load_json(self.file_tmp_last_chrome_session)
        return {}

    def set_last_chrome_session(self, data):
        Json.save_json_pretty(self.file_tmp_last_chrome_session, data)
        return self

    # helper sync functions

    def sync__setup_browser(self):                                                          # weirdly this works but the version below (using @sync) doesn't (we get an 'Read-only file system' error)
        import asyncio
        if os.getenv('AWS_REGION') is None:                                                 # we not in AWS so run the normal browser connect using pyppeteer normal method
            asyncio.get_event_loop().run_until_complete(self.browser_connect())
            return self

        load_dependency('pyppeteer')
        path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'     # path to headless_shell AWS Linux executable
        os.environ['PYPPETEER_HOME'] = '/tmp'                                                   # tell pyppeteer to use this read-write path in Lambda aws

        async def set_up_browser():
            from pyppeteer import launch                                                        # import pyppeteer dependency
            Process.run("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
            self._browser = await launch(executablePath=path_headless_shell,                    # lauch chrome (i.e. headless_shell)
                                         args=['--no-sandbox'              ,                                               '--single-process'         ])                             # two key settings or the requests will not work
        asyncio.get_event_loop().run_until_complete(set_up_browser())
        return self

    # @sync
    # async def sync__setup_aws_browser(self):
    #
    #     load_dependency('pyppeteer')
    #     from pyppeteer import launch
    #     path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'
    #     os.environ['PYPPETEER_HOME'] = '/tmp'
    #     Process.run("chmod", ['+x', path_headless_shell])
    #     self._browser = await launch(executablePath=path_headless_shell,
    #                                  args=['--no-sandbox',
    #                                        '--single-process'])
    #     return self

    @sync
    async def sync__browser_width(self, width,height=None):
        if height is None: height = width
        return await self.page_size(width, height)

    @sync
    async def sync__close_browser(self):
        await self._browser.close()
        return self

    @sync
    async def sync__js_execute(self, js_code):
        return await self.js_execute(js_code)

    @sync
    async def sync_js_invoke_function(self,name, params=None):
        return await self.js_invoke_function(name, params)

    @sync
    async def sync_js_assign_variable(self, variable, data=None):
        return await self.js_assign_variable(variable,data)

    @sync
    async def sync__html_raw(self):
        return await self.html_raw()

    @sync
    async def sync__open(self, url):
        await self.open(url)
        return self

    @sync
    async def sync__url(self):
        return await self.url()

    @sync
    async def sync__screenshot(self, url=None,file_screenshot = None,clip=None):
        return await self.screenshot(url,file_screenshot = file_screenshot,clip=clip)

    @sync
    async def sync__screenshot_base64(self, url=None,full_page=True,close_browser=False, clip=None,delay=None):
        screenshot_file = await self.screenshot(url=url,full_page=full_page, clip=clip, delay=delay)
        return base64.b64encode(open(screenshot_file, 'rb').read()).decode()

    @sync
    async def sync__await_for_element(self, selector, timeout=10000):
        page = await self.page()
        try:
            await page.waitForSelector(selector, {'timeout': timeout })
            return True
        except Exception as error:
            Dev.print("[Errpr][sync__await_for_element] {0}".format(error))
            return False

import asyncio
import base64
import os

from utils.Process import Process
from utils.aws.Lambdas import load_dependency


class Browser_Commands:

    @staticmethod
    def run_pyppeteer(target_url):
        load_dependency('pyppeteer')
        path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  # path to headless_shell AWS Linux executable
        path_page_screenshot         = '/tmp/screenshot.png'  # path to store screenshot of url loaded
        os.environ['PYPPETEER_HOME'] = '/tmp'  # tell pyppeteer to use this read-write path in Lambda aws
        #target_url                  = 'http://localhost:1234/map/simple'
        web_root = '/tmp/html'

        async def take_screenshot():
            from pyppeteer import launch  # import pyppeteer dependency
            Process.run("chmod", ['+x', path_headless_shell])  # set the privs of path_headless_shell to execute
            browser = await launch(executablePath=path_headless_shell,  # lauch chrome (i.e. headless_shell)
                                   args=['--no-sandbox',
                                         '--single-process'])  # two key settings or the requests will not work

            page = await browser.newPage()  # typical pyppeteer code, where we create a new Page object
            await page.goto(target_url)  # - open an url

            # await page.waitFor(2 * 1000);

            await page.screenshot(
                {'path': path_page_screenshot, 'fullPage': True})  # - take a screenshot of the page loaded and save it
            # await page.pdf({'path': path_page_screenshot});
            await browser.close()

        asyncio.get_event_loop().run_until_complete(take_screenshot())
        base64_data = base64.b64encode(open(path_page_screenshot, 'rb').read()).decode()

        return {'isBase64Encoded': True,
                'statusCode': 200,
                'headers': {'Content-Type': 'image/png'},
                'body': base64_data}  # base64_encoded_binary_data}

        return 'done for {0}'.format(target_url)

    @staticmethod
    def screenshot_url(team_id, channel, params):
        url = params.pop()
        return Browser_Commands.run_pyppeteer(url)
import asyncio
import base64
import os

from utils.Files import Files
from utils.Lambdas_Helpers import slack_message
from utils.Process import Process
from utils.aws.Lambdas import load_dependency, Lambdas
from utils.aws.s3 import S3


class Browser_Commands:

    # @staticmethod
    # def run_pyppeteer(target_url):
    #     load_dependency('pyppeteer')
    #     path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  # path to headless_shell AWS Linux executable
    #     path_page_screenshot         = '/tmp/screenshot.png'  # path to store screenshot of url loaded
    #     os.environ['PYPPETEER_HOME'] = '/tmp'  # tell pyppeteer to use this read-write path in Lambda aws
    #
    #     async def take_screenshot():
    #         from pyppeteer import launch  # import pyppeteer dependency
    #         Process.run("chmod", ['+x', path_headless_shell])  # set the privs of path_headless_shell to execute
    #         browser = await launch(executablePath=path_headless_shell,  # lauch chrome (i.e. headless_shell)
    #                                args=['--no-sandbox',
    #                                      '--single-process'])  # two key settings or the requests will not work
    #
    #         page = await browser.newPage()  # typical pyppeteer code, where we create a new Page object
    #         await page.goto(target_url)  # - open an url
    #
    #         # await page.waitFor(2 * 1000);
    #
    #         await page.screenshot(
    #             {'path': path_page_screenshot, 'fullPage': True})  # - take a screenshot of the page loaded and save it
    #         # await page.pdf({'path': path_page_screenshot});
    #         await browser.close()
    #
    #     asyncio.get_event_loop().run_until_complete(take_screenshot())
    #     base64_data = base64.b64encode(open(path_page_screenshot, 'rb').read()).decode()
    #
    #     return base64_data

    @staticmethod
    def _get_png_data_from_url_screenshot(url):
        if not url: return ''
        load_dependency('syncer')
        from browser.API_Browser import API_Browser
        return API_Browser().sync__setup_aws_browser()          \
                            .sync__screenshot_base64(url,close_browser=True)

    @staticmethod
    def screenshot_png(team_id, channel, params):
        #slack_message('screenshot_url for: `{0}`'.format(url), [], channel, team_id)
        return Browser_Commands._get_png_data_from_url_screenshot(params.pop(0))

    @staticmethod
    def screenshot(team_id, channel, params):
        s3_bucket    = 'gs-lambda-tests'
        url          = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
        slack_message(":point_right: taking screenshot of url: {0}".format(url),[], channel,team_id)

        png_data     = Browser_Commands._get_png_data_from_url_screenshot(url)
        png_file     = Files.temp_file('.png')
        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        s3_key = S3().file_upload_as_temp_file(png_file, s3_bucket)
        png_to_slack = Lambdas('utils.png_to_slack')
        payload      = { 's3_bucket': s3_bucket, 's3_key':s3_key, 'team_id':team_id, 'channel': channel, 'title': url }
        png_to_slack.invoke_async(payload)
        return "stats", [{ 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') }]

        return None,None

    @staticmethod
    def lambda_status(team_id, channel, params):
        text = "Here are the current status of the `graph` lambda function"
        attachments = []
        attachments.append({ 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') })
        attachments.append({'title': 'Temp Files', 'text': Process.run("ls", ["-ls",'/tmp']).get('stdout') })
        #attachments.append({'title': 'Processes', 'text': )
        return text,attachments
# return data, \
#        Process.run("ps",["-A"]).get('stdout'), \
#        Files.find('/tmp/core.headless_shell.*')
#        #Process.run("ls", ["-ls",'/tmp']).get('stdout'), \


# @staticmethod
    # def use_api_browser(team_id, channel, params):
    #     load_dependency('syncer')
    #     from browser.API_Browser import API_Browser
    #
    #     url = params.pop()
    #     api_browser = API_Browser()
    #
    #     return (
    #               api_browser.sync__setup_aws_browser()
    #                          #.sync__open(url)
    #                          .sync__screenshot_base64(url)
    #                          #.sync__html_raw()
    #                          #.sync__url()
    #
    #            )

    # @staticmethod
    # def setup_aws_browser():
    #     from utils.aws.Lambdas import load_dependency
    #     load_dependency('pyppeteer')
    #
    #     import asyncio
    #
    #     path_headless_shell = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'  # path to headless_shell AWS Linux executable
    #     path_page_screenshot = '/tmp/screenshot.png'  # path to store screenshot of url loaded
    #     os.environ['PYPPETEER_HOME'] = '/tmp'  # tell pyppeteer to use this read-write path in Lambda aws
    #     # target_url                  = 'http://localhost:1234/map/simple'
    #     web_root = '/tmp/html'
    #
    #     async def take_screenshot():
    #         from pyppeteer import launch  # import pyppeteer dependency
    #         Process.run("chmod", ['+x', path_headless_shell])  # set the privs of path_headless_shell to execute
    #         browser = await launch(executablePath=path_headless_shell,  # lauch chrome (i.e. headless_shell)
    #                                args=['--no-sandbox',
    #                                      '--single-process'])  # two key settings or the requests will not work
    #
    #         page = await browser.newPage()  # typical pyppeteer code, where we create a new Page object
    #
    #     asyncio.get_event_loop().run_until_complete(take_screenshot())
    #
    #     return 'here 13'
    #     return 'here'


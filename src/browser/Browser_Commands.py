import asyncio
import base64
import os

from utils.Dev import Dev
from utils.Files import Files
from utils.Lambdas_Helpers import slack_message
from utils.Process import Process
from utils.aws.Lambdas import load_dependency, Lambdas
from utils.aws.s3 import S3


class Browser_Commands:

    # helper methods (to refactor to another class
    @staticmethod
    def _get_png_data_from_url_screenshot(url):
        if not url: return ''
        load_dependency('syncer')
        from browser.API_Browser import API_Browser
        return API_Browser().sync__setup_aws_browser()          \
                            .sync__screenshot_base64(url,close_browser=True)

    @staticmethod
    def _send_to_slack(team_id, channel, url, png_data):
        s3_bucket = 'gs-lambda-tests'
        png_file = Files.temp_file('.png')
        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        s3_key = S3().file_upload_as_temp_file(png_file, s3_bucket)
        png_to_slack = Lambdas('utils.png_to_slack')
        payload = {'s3_bucket': s3_bucket, 's3_key': s3_key, 'team_id': team_id, 'channel': channel, 'title': url}
        png_to_slack.invoke_async(payload)

    @staticmethod
    def screenshot_png(team_id, channel, params):
        #slack_message('screenshot_url for: `{0}`'.format(url), [], channel, team_id)
        return Browser_Commands._get_png_data_from_url_screenshot(params.pop(0))

    @staticmethod
    def screenshot(team_id, channel, params):
        url          = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
        slack_message(":point_right: taking screenshot of url: {0}".format(url),[], channel,team_id)

        png_data     = Browser_Commands._get_png_data_from_url_screenshot(url)
        Browser_Commands._send_to_slack(team_id,channel, url, png_data)
        return "stats", [{ 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') }]

        return None,None

    @staticmethod
    def lambda_status(team_id, channel, params):
        text = "Here are the current status of the `graph` lambda function"
        attachments = []
        attachments.append({ 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') })
        attachments.append({'title': 'Temp Files', 'text': Process.run("ls", ["-ls",'/tmp']).get('stdout') })
        return text,attachments

    @staticmethod
    def render_file(team_id, channel, params):
        load_dependency('syncer')
        load_dependency('requests')
        if params:
            url = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
        from browser.API_Browser import API_Browser
        from browser.Render_Page import Render_Page
        api_browser = API_Browser().sync__setup_aws_browser()
        render_page = Render_Page(api_browser)
        content = render_page.render_html("<h1>an test 123<h1>")
        api_browser.sync__close_browser()
        Dev.pprint(Process.run("ps", ["-A"]).get('stdout'))
        return content

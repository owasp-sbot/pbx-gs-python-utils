import base64
import os
from utils.Files import Files
from utils.aws.Lambdas import load_dependency, Lambdas
from utils.aws.s3 import S3


class Browser_Lamdba_Helper:
    def __init__(self, headless = True):
        self.api_browser = None
        self.render_page = None
        self.headless    = headless
        self.auto_close  = headless


    def get_screenshot_png(self,url=None, clip=None,full_page=None,close_browser=True, delay=None):
        load_dependency('syncer')
        return self.api_browser.sync__screenshot_base64(url, close_browser=close_browser, clip=clip,full_page=full_page,delay=delay)

    def open_local_file(self, path, js_code=None):
        return self.open_local_page_and_get_html(path,js_code)

    def open_local_page_and_get_html(self, path, js_code=None):
        with self.render_page.web_server as web_server:
           url      = web_server.url(path)
           return self.render_page.get_page_html_via_browser(url, js_code=js_code)

    def open_local_page_and_get_screenshot(self, path, png_file=None,js_code=None,clip=None, delay=None):
        with self.render_page.web_server as web_server:
           url      = web_server.url(path)
           return self.render_page.get_screenshot_via_browser(url, js_code=js_code, clip=clip,png_file=png_file,delay=delay)

    def render_file(self,team_id, channel, path,js_code=None,clip=None, delay=None):
        png_file = self.open_local_page_and_get_screenshot(path=path, js_code=js_code,clip=clip, delay=delay)
        return self.send_png_file_to_slack(team_id, channel, 'markdown', png_file)

    def send_png_file_to_slack(self, team_id, channel, target, png_file):
        if team_id and channel:
            s3_bucket    = 'gs-lambda-tests'
            s3_key       = S3().file_upload_as_temp_file(png_file, s3_bucket)
            png_to_slack = Lambdas('utils.png_to_slack')
            payload = {'s3_bucket': s3_bucket, 's3_key': s3_key, 'team_id': team_id, 'channel': channel, 'title': target }
            png_to_slack.invoke_async(payload)
            return None, None
        else:
            return base64.b64encode(open(png_file, 'rb').read()).decode()

    def send_png_data_to_slack(self, team_id, channel, target, png_data):
        png_file = Files.temp_file('.png')
        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        return self.send_png_file_to_slack(team_id, channel,target, png_file)

    def setup(self):

        if os.getenv('AWS_REGION'):
            load_dependency('syncer')
            load_dependency('requests')
            #self.setup_AWS()
        # else:
        #     self.setup_local()

        from browser.API_Browser import API_Browser
        from browser.Render_Page import Render_Page
        self.api_browser = API_Browser(headless=self.headless, auto_close=self.auto_close).sync__setup_browser()
        self.render_page = Render_Page(api_browser=self.api_browser, web_root=self.web_root())

        return self

    @staticmethod
    def save_png_data(png_data, png_file=None):
        try:
            if png_file is None:
                png_file = '/tmp/lambda_png_file.png'
            if png_data:
                with open(png_file, "wb") as fh:
                    fh.write(base64.decodebytes(png_data.encode()))
                return "Png data with size {0} saved to {1}".format(len(png_data),png_file)
        except Exception as error:
            return "[_save_png_file][Error] {0}\n\n".format(error,png_data)

    # def setup_AWS(self):
    #     load_dependency('syncer')
    #     load_dependency('requests')

    # def setup_local(self):
    #     return

    def web_root(self):
        if os.getenv('AWS_REGION') is not None:         # if we are in AWS
            return Files.path_combine('.','./web_root')
        if 'test/browser' in Files.current_folder():    # if we are in an unit test
            return  Files.path_combine('.','../../../../src/web_root')
        parent_folder = Files.folder_name(__file__)
        if 'pbx-gs-python-utils/src/browser' in parent_folder:
            return Files.path_combine(parent_folder,'../../../../src/web_root')
        return None
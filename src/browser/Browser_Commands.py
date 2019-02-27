from time import sleep

from browser.Browser_Lamdba_Helper  import Browser_Lamdba_Helper
from utils.Files                    import Files
from utils.Lambdas_Helpers          import slack_message
from utils.Process                  import Process
from utils.aws.Lambdas              import load_dependency, Lambdas
from utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


class Browser_Commands:

    # helper methods (to refactor to another class
    # @staticmethod
    # def _get_png_data_from_url_screenshot(url):
    #     if not url: return ''
    #     load_dependency('syncer')
    #     from browser.API_Browser import API_Browser
    #     return API_Browser().sync__setup_browser()          \
    #                         .sync__screenshot_base64(url,close_browser=True)

    # @staticmethod
    # def _send_to_slack__png_file(team_id, channel, target, png_file):
    #     if team_id and channel:
    #         Browser_Commands._send_to_slack_png_file(team_id, channel, target, png_file)
    #         #Browser_Commands._send_to_slack(team_id, channel, target, png_data)
    #         return None, None
    #     else:
    #         return base64.b64encode(open(png_file, 'rb').read()).decode()

    # @staticmethod
    # def _send_to_slack(team_id, channel, url, png_data):
    #
    #     png_file = Files.temp_file('.png')
    #     with open(png_file, "wb") as fh:
    #         fh.write(base64.decodebytes(png_data.encode()))
    #     Browser_Commands._send_to_slack_png_file(team_id, channel, url, png_file)

    # @staticmethod
    # def _send_to_slack_png_file(team_id, channel, url, png_file):
    #     if team_id and channel:
    #

    #@staticmethod
    #def screenshot_png(team_id, channel, params):
    #    #slack_message('screenshot_url for: `{0}`'.format(url), [], channel, team_id)
    #    url = params.pop(0)
    #    return Browser_Lamdba_Helper().setup().get_screenshot_png(url)

        #return Browser_Commands._get_png_data_from_url_screenshot()

    @staticmethod
    def screenshot(team_id=None, channel=None, params=[]):
        url          = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
        slack_message(":point_right: taking screenshot of url: {0}".format(url),[], channel,team_id)
        browser_helper = Browser_Lamdba_Helper().setup()
        png_data       = browser_helper.get_screenshot_png(url)
        return browser_helper.send_png_data_to_slack(team_id,channel,url, png_data)

    @staticmethod
    def lambda_status(team_id, channel, params):
        text        = "Here are the current status of the `graph` lambda function"
        attachments = [ { 'title':'Processes','text'  : Process.run("ps", ["-A"]        ).get('stdout') },
                        {'title': 'Temp Files', 'text': Process.run("ls", ["-ls",'/tmp']).get('stdout') }]
        return text,attachments

    @staticmethod
    def list(team_id, channel, params):
        text = "Here are the current examples files:"
        attachments = []
        files       = ''
        for file in Files.find('./web_root/**/*.html'):
            files += '{0} \n'.format(file.replace('./web_root/',''))
        attachments.append({'text': files })
        return text, attachments

    @staticmethod
    def markdown(team_id, channel, params):
        path  = 'examples/markdown.html'
        js_code = {'name': 'convert', 'params': '# Markdown code!!! \n 123 \n - bullet point \n - another one ![](http://visjs.org/images/gettingstartedSlide.png)'}
        if params and len(params) > 0:
            js_code['params']= ' '.join(params).replace('```','')

        return Browser_Lamdba_Helper().setup()                                   \
                                      .render_file(team_id, channel, path,js_code)

    @staticmethod
    def render(team_id, channel, params):

        if params:
            target = params.pop(0)
            if len(params) == 4:
                clip = {'x': int(params[0]), 'y': int(params[1]), 'width': int(params[2]), 'height': int(params[3])}
            else:
                clip = None
        else:
            return None

        slack_message(":point_right: rendering file `{0}`".format(target), [], channel, team_id)
        return Browser_Lamdba_Helper().setup().render_file(team_id, channel, target,clip=clip)

        #png_file = browser_helper.render_page.screenshot_file_in_folder(browser_helper.web_root(), target, clip=clip)
        #return browser_helper.send_png_file_to_slack(team_id, channel, target, png_file)

        # return None
        # load_dependency('syncer')
        # load_dependency('requests')
        # from browser.API_Browser import API_Browser
        # from browser.Render_Page import Render_Page
        #
        # web_root = './web_root/'
        # target   = url_path
        #
        # api_browser = API_Browser().sync__setup_browser()
        # render_page = Render_Page(api_browser)
        #
        # browser_helper = Browser_Lamdba_Helper().setup()
        # png_file = render_page.screenshot_file_in_folder(web_root, target, clip=clip)
        #
        # return browser_helper.send_png_file_to_slack(team_id, channel, 'markdown', png_file)
        # #return Browser_Commands._send_to_slack__png_file(team_id, channel, target, png_file)

    @staticmethod
    def vis_js(team_id=None, channel=None, params=None):
        path = 'examples/vis-js.html'
        if params and len(params) > 0:
            js_code = params.pop(0)
        else:
            js_code= """
                        network.body.data.nodes.add({id:'12',label:'new Dynamic Node'})
                        network.body.data.edges.add({from:'12',to:'1'})
                    """
        browser = Browser_Lamdba_Helper().setup()

        return browser.open_local_page_and_get_html(path,js_code=js_code)

        #return browser.render_file(team_id, channel,path, js_code=js_code)

    @staticmethod
    def elk(team_id=None, channel=None, params=None):
        load_dependency('syncer')
        from browser.sites.Site_ELK import ELK_Commands
        from browser.sites.Site_ELK import Site_ELK

        if len(params) == 0:
            Slack_Commands_Helper(ELK_Commands).invoke(team_id, channel, params)
            return None

        browser_helper = Browser_Lamdba_Helper().setup()
        elk = Site_ELK(browser_helper.api_browser, team_id, channel)

        elk.sync__connect_and_login()

        params.append(browser_helper)
        params.append(elk)

        result = Slack_Commands_Helper(ELK_Commands).invoke(team_id, channel, params)

        if team_id:
            return None
        else:
            return result

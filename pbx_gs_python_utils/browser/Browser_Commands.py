from browser.Browser_Lamdba_Helper      import Browser_Lamdba_Helper
from utils.Files                        import Files
from utils.Lambdas_Helpers              import slack_message
from utils.Misc import Misc
from utils.Process                      import Process
from utils.aws.Lambdas                  import load_dependency
from utils.slack.Slack_Commands_Helper  import Slack_Commands_Helper


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
        delay        = Misc.to_int(Misc.array_pop(params,0))
        slack_message(":point_right: taking screenshot of url: {0}".format(url),[], channel,team_id)
        browser_helper = Browser_Lamdba_Helper().setup()
        png_data       = browser_helper.get_screenshot_png(url,full_page=True, delay=delay)
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
            delay  = Misc.to_int(Misc.array_pop(params,0))
            if len(params) == 4:
                clip = {'x': int(params[0]), 'y': int(params[1]), 'width': int(params[2]), 'height': int(params[3])}
            else:
                clip = None
        else:
            return None

        slack_message(":point_right: rendering file `{0}`".format(target), [], channel, team_id)
        return Browser_Lamdba_Helper().setup().render_file(team_id, channel, target,clip=clip, delay=delay)

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

    # @staticmethod
    # def risks(team_id=None, channel=None, params=None):
    #     path = '/gs/risk/r1-and-r2.html'
    #     data = {}
    #     if params and len(params) > 0:
    #         fixed_params = ' '.join(params).replace('```','')
    #         data = {}
    #         for items in fixed_params.split(','):
    #             values = items.split(':')
    #             data[values[0].strip()] = values[1].strip()
    #
    #     js_code = "r1_and_r2.set_risks({0})".format(json.dumps(data))
    #     clip = {'x': 1, 'y': 1, 'width': 915, 'height': 435}
    #     browser = Browser_Lamdba_Helper().setup()
    #     return browser.render_file(team_id, channel, path=path, js_code=js_code, clip=clip)

        #return browser.open_local_page_and_get_screenshot(path, js_code=js_code, png_file=png_file)

        #
        #.set_risks({'r1_2': '1', 'r2_4': '0', 'r5_4': '2'})

    @staticmethod
    def risks(team_id=None, channel=None, params=None):
        load_dependency('syncer') ;
        load_dependency('requests')

        from view_helpers.Risk_Dashboard import Risk_Dashboard

        jira_key = params.pop(0)

        return ( Risk_Dashboard().create_dashboard_for_jira_key(jira_key)
                                 .send_graph_name_to_slack(team_id, channel)
                                 .send_screenshot_to_slack(team_id, channel))

        # graph_name = 'graph_DGK'
        # root_node = 'GSSP-6'
        #
        # return Risk_Dashboard().create_dashboard_for_graph(graph_name,root_node).send_screenshot_to_slack(team_id, channel)


    @staticmethod
    def risks_test_data(team_id=None, channel=None, params=None):
        load_dependency('syncer') ;
        load_dependency('requests')

        from view_helpers.Risk_Dashboard import Risk_Dashboard

        return Risk_Dashboard().create_dashboard_with_test_data().send_screenshot_to_slack(team_id, channel)

        #browser = Risk_Dashboard().create_dashboard_with_test_data().browser()

        #clip = {'x': 1, 'y': 1, 'width': 915, 'height': 435}
        #png_file =  browser.sync__screenshot(clip = clip)
        #return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'markdown', png_file)


    # @staticmethod
    # def vis_js(team_id=None, channel=None, params=None):
    #     path = 'examples/vis-js.html'
    #
    #     params = ' '.join(params).replace('“','"').replace('”','"')
    #     data = json.loads(params)
    #
    #     load_dependencies(['syncer', 'requests'])
    #
    #     nodes   = data.get('nodes'  )
    #     edges   = data.get('edges'  )
    #     options = data.get('options')
    #     from view_helpers.Vis_Js import Vis_Js
    #     vis_js = Vis_Js()
    #     vis_js.create_graph(nodes, edges, options)
    #     #vis_js.show_jira_graph(graph_name)
    #     return vis_js.send_screenshot_to_slack(team_id,channel)
    #
    #     # browser = Browser_Lamdba_Helper().setup()
    #     #
    #     # return browser.open_local_page_and_get_html(path,js_code=js_code)
    #
    #     #return browser.render_file(team_id, channel,path, js_code=js_code)


    @staticmethod
    def am_charts(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `am_charts` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from view_helpers.Am_Charts_Views import Am_Charts_Views
        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(Am_Charts_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def calendar(team_id=None, channel=None, params=None):
        from view_helpers.Full_Calendar_Views import Full_Calendar_Views
        #params[0], params[1] = params[1], params[0]
        Slack_Commands_Helper(Full_Calendar_Views).show_duration(True).invoke(team_id, channel,params)


    @staticmethod
    def go_js(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `go_js` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from view_helpers.Go_Js_Views import Go_Js_Views
        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(Go_Js_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def graph(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `graph` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text,[{'text': attachment_text}]

        from view_helpers.Vis_Js_Views import Vis_Js_Views

        params[0],params[1] = params[1],params[0]       # swap items (since it is more user friendly to add the graph name first)

        (text, attachments) = Slack_Commands_Helper(Vis_Js_Views).show_duration(False).invoke(team_id, channel, params)

        if team_id is None:
            return text

    @staticmethod
    def viva_graph(team_id=None, channel=None, params=None):
        if len(params) < 2:
            text = ':red_circle: Hi, for the `viva_graph` command, you need to provide 2 parameters: '
            attachment_text = '*graph name* - the nodes and edges you want to view\n' \
                              '*view name* - the view to render'
            return text, [{'text': attachment_text}]

        from view_helpers.VivaGraph_Js_Views import VivaGraph_Js_Views

        params[0], params[1] = params[1], params[0]

        (text, attachments) = Slack_Commands_Helper(VivaGraph_Js_Views).show_duration(True).invoke(team_id, channel, params)

        if team_id is None:
            return text

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

    @staticmethod
    def table(team_id=None, channel=None, params=None):

        if len(params) < 2:
            text = ':red_circle: Hi, for the `table` command, you need to provide 2 parameters: '
            attachment_text = '*target* - the jira id or graph to get\n' \
                              '*view name* - the view to render'
            return text,[{'text': attachment_text}]

        from view_helpers.DataTable_Js_Views import DataTable_Js_Views

        params[0],params[1] = params[1],params[0]       # swap items (since it is more user friendly to add the graph name first)

        (text, attachments) = Slack_Commands_Helper(DataTable_Js_Views).show_duration(False).invoke(team_id, channel, params)

        if team_id is None:
            return text
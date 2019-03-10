import base64
import json
import os
from unittest import TestCase

from browser.Browser_Commands import Browser_Commands
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Browser_Commands(TestCase):

    def setUp(self):
        self.browser_commands = Browser_Commands()
        self.team_id = 'T7F3AUXGV'
        self.channel = 'DDKUZTK6X'

    def _save_png_data(self, png_data):
        png_file = '/tmp/lambda_png_file.png'
        if png_data:
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(png_data.encode()))

    def test_list(self):
        result = self.browser_commands.list(None, None, None)
        Dev.pprint(result)

    def test_screenshot(self):
        #os.environ['OSX_CHROME'] = 'True'
        team_id = 'T7F3AUXGV'
        channel = 'DDKUZTK6X'
        url = 'https://www.google.co.uk'
        self.browser_commands.screenshot(team_id, channel, [url])

    def test_screenshot__localhost(self):
        url = 'http://localhost:12345'
        png_data = self.browser_commands.screenshot(None, None, params = [url])
        self._save_png_data(png_data)

    def test_render(self):
        params = ['/examples/bootstrap-cdn.html']
        params   = ['examples/wardley_map/cup-of-tea.html']
        png_data = self.browser_commands.render(None,None,params)
        #Dev.print(png_data)
        self._save_png_data(png_data)

    def test_render__with_clip_params(self):
        params = ['/examples/bootstrap-cdn.html'        ,0  ,0 ,500 ,50 ]
        params = ['examples/wardley_map/cup-of-tea.html',250,50,600 ,200]
        png_data = self.browser_commands.render(None,None,params)
        #Dev.print(png_data)
        self._save_png_data(png_data)


    def test_markdown___no_params(self):
        result = self.browser_commands.markdown(None,None,None)
        self._save_png_data(result)
        #Dev.pprint(result)

    def test_markdown___with_params(self):
        params = ["# Created from unit test \n","2nd paragraph --- 123"]
        result = self.browser_commands.markdown(None,None,params)
        self._save_png_data(result)

    def test_risk(self):
        params = ['GSSP-6']
        params = ['GSSP-113']
        result = self.browser_commands.risks(params=params)
        self._save_png_data(result)

    def test_vis_js(self):
        nodes = [{'id': '123', 'label': 'this is a label\n in two lines'},
                 {'id': 'aaa', 'label': '123'}]
        edges = [{'from': '123', 'to': 'aaa'}]

        options = { 'nodes' : { 'shape' : 'box' } }
        data = { 'nodes':nodes , 'edges':edges , 'options': options}

        params = [json.dumps(data)]

        #self.vis_js.create_graph(nodes, edges, options)
        result = self.browser_commands.vis_js(params=params)
        #Dev.pprint(result)
        self._save_png_data(result)

    def test_graph(self):
        graph_name = 'graph_XKW'
        params = [graph_name,'default']
        result = self.browser_commands.graph(params=params)
        Dev.pprint(result)
        self._save_png_data(result)

    def test_graph__view__node_label(self):
        graph_name = 'graph_DEQ'
        params = [graph_name,'node_label', 'Labels']
        result = self.browser_commands.graph(params=params)
        Dev.pprint(result)
        self._save_png_data(result)


    def test_table(self):
        result = self.browser_commands.table()
        Dev.pprint(result)
        self._save_png_data(result)

    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()
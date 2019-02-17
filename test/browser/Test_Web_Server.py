from unittest import TestCase
from browser.Web_Server import Web_Server
from utils.Dev import Dev


class Test_Web_Server(TestCase):
    def setUp(self):
        self.web_server = Web_Server()
        self.web_server.start()

    def test_path_to_file(self):
        assert self.web_server.path_to_file(''                ) == '/tmp/temp_web_server/html'
        assert self.web_server.path_to_file('/123456'         ) == '/tmp/temp_web_server/html/123456'
        assert self.web_server.path_to_file('bbbb.html'       ) == '/tmp/temp_web_server/html/bbbb.html'
        assert self.web_server.path_to_file('aaa/bbb/ccc.html') == '/tmp/temp_web_server/html/aaa/bbb/ccc.html'
        assert self.web_server.path_to_file('../../abc.html'  ) == '/tmp/abc.html'                                 # path traversal vulnerability
        assert self.web_server.path_to_file('..\\..\\abc.html') == '/tmp/temp_web_server/html/..\\..\\abc.html'

    def tearDown(self):
        self.web_server.stop()

    def test_start_server(self):
        html = self.web_server.html('')
        assert '</html>' in html
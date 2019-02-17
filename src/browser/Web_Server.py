import subprocess
from time import sleep

import requests

from utils.Dev import Dev
from utils.Files import Files
from utils.Misc  import Misc
from utils.Http  import GET,port_is_open


class Web_Server:
    def __init__(self):
        self.src_tmp     = '/tmp/temp_web_server'
        self.web_root    = self.src_tmp + '/html'
        self.html_file   = Files.path_combine(self.web_root, 'index.html')
        self.port        = Misc.random_number(10000,60000)
        self.server_proc = None

    def html(self, path=''):
        Dev.pprint(self.url()+ path)
        return requests.get(self.url(path)).text
        #GET(self.url()+ path)

    def path_to_file(self, file_path):                                  # has path traversal vulnerability
        if file_path and len(file_path) >0 and file_path[0] == '/':
            file_path = file_path[1:]
        return Files.path_combine(self.web_root, file_path)

    def start(self):
        if Files.not_exists(self.web_root):  Files.folder_create(self.web_root)     # make sure root folder exists
        self.server_proc = subprocess.Popen(["python", "-m", "SimpleHTTPServer", str(self.port)], cwd=self.web_root)
        self.wait_for_server_started()
        return self

    def stop(self):
        self.server_proc.kill()

    def url(self,path=''):
        return 'http://localhost:{0}/{1}'.format(self.port, path)

    def wait_for_server_started(self, max_number_of_tries = 30):           # 0.75 of a Sec should be enough to start the server
        while max_number_of_tries > 0:
            max_number_of_tries -= 1
            sleep(0.025)                            # wait 0.025 of a second (0.025 * 30 = 0.75 sec)
            if port_is_open(self.port):
                return True
        return False

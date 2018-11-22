import base64
import subprocess
import tempfile
from os.path import abspath, join,basename

import requests

from utils.Dev import Dev
from utils.Files import Files
#from utils.Show_Img import Show_Img
from utils.aws.Lambdas import Lambdas


class API_Plant_UML:

    def __init__(self):
        self.url_plantuml_server = 'http://localhost:8080/form'
        self.tmp_png_file        = Files.temp_file('.png')

    def puml_to_png(self,puml):
        return self.puml_to_png_using_lambda_function(puml)  # default to using lambda function
        #return self.puml_to_png_via_local_server(puml)      # using local server

    def puml_to_png_via_local_server(self, puml,target_file = None):
        if target_file is None: target_file = self.tmp_png_file
        data         = { "text"    :  puml }
        url          = requests.post(self.url_plantuml_server, data = data).url
        url_png      = url.replace('/uml/', '/png/')
        response     = requests.get(url_png)
        with open(self.target_file, 'wb') as f:
            f.write(response.content)
        return self.target_file

        response = requests.get(url)
        if response.status_code == 200:
            with open(tmp_png_file, 'wb') as f:
                f.write(response.content)
        return tmp_png_file

    def puml_to_png_using_lambda_function(self,puml, target_file = None):
        if target_file is None : target_file = self.tmp_png_file
        puml_to_png  = Lambdas('utils.puml_to_png').invoke
        result       = puml_to_png({"puml": puml})
        with open(target_file, "wb") as fh:
            fh.write(base64.decodebytes(result['png_base64'].encode()))
        return target_file

    # def puml_to_png_using_local_jar_file(self, puml):
    #     (fd, tmp_file) = tempfile.mkstemp('.puml')
    #     png_file       = "/tmp/{0}".format(basename(tmp_file)).replace('.puml','.png')
    #     Files.write(tmp_file, puml)
    #     self.exec_jar_plantuml(['-tpng', '-o', '/tmp', tmp_file])
    #     return png_file


















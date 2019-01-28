
import json
import  unittest
from    utils.Dev              import Dev
from    utils.aws.Lambdas      import Lambdas


class Test_Lambda_log_to_elk(unittest.TestCase):
    def setUp(self):
        #path_libs = '../_lambda_dependencies/elastic'
        self.log_to_elk = Lambdas('utils.log_to_elk')#, path_libs = path_libs)

    def test_update_invoke(self):
        payload = {}
        result = self.log_to_elk.update().invoke(payload)
        Dev.pprint(result)

    def test_invoke___check_multiple_log_options(self):
        self.log_to_elk.invoke({ 'level': 'info' , 'category': 'category info' , 'message': 'message info' , 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'debug', 'category': 'category debug', 'message': 'message debug', 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'error', 'category': 'category error', 'message': 'message error', 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'debug'})
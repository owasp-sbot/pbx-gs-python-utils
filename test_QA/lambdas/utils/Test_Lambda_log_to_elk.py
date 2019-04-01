
import json
import  unittest

from    pbx_gs_python_utils.lambdas.utils.log_to_elk    import run
from    pbx_gs_python_utils.utils.Dev                   import Dev
from    pbx_gs_python_utils.utils.aws.Lambdas           import Lambdas


class Test_Lambda_log_to_elk(unittest.TestCase):
    def setUp(self):
        self.log_to_elk = Lambdas('pbx_gs_python_utils.lambdas.utils.log_to_elk')

    def test_invoke_directly(self):
        assert run({},{}) is None

    #def test_update_invoke(self):
    #    assert self.log_to_elk.update_with_lib().invoke({}) is None

    def test_invoke___check_multiple_log_options(self):
        self.log_to_elk.invoke({ 'level': 'info' , 'category': 'category info' , 'message': 'message info' , 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'debug', 'category': 'category debug', 'message': 'message debug', 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'error', 'category': 'category error', 'message': 'message error', 'data': {'answer' : 42}})
        self.log_to_elk.invoke({ 'level': 'debug'})
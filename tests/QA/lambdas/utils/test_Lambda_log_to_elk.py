
import  unittest

from osbot_aws.apis.Lambda import Lambda

from    pbx_gs_python_utils.lambdas.utils.log_to_elk    import run
from    pbx_gs_python_utils.utils.Dev                   import Dev


class Test_Lambda_log_to_elk(unittest.TestCase):
    def setUp(self):
        self.log_to_elk = Lambda('pbx_gs_python_utils.lambdas.utils.log_to_elk')

    def test_invoke_directly(self):
        assert run({},{}) is None

    # def test_update_invoke(self):
    #     payload = {'message' : 'an message'}
    #     response = self.log_to_elk.update_with_lib().invoke(payload)
    #
    #     Dev.pprint(response)
    #     #assert response.get('elastic_response').get('result') == 'created'
    #
    #     #assert self.log_to_elk.update_with_lib().invoke({}) is None

    def test_invoke___check_multiple_log_options(self):
        response = self.log_to_elk.invoke({ 'level': 'info' , 'category': 'category info' , 'message': 'message info' , 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'
        response = self.log_to_elk.invoke({ 'level': 'debug', 'category': 'category debug', 'message': 'message debug', 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'
        response = self.log_to_elk.invoke({ 'level': 'error', 'category': 'category error', 'message': 'message error', 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'

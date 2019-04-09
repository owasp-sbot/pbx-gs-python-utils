import unittest

from pbx_gs_python_utils.utils.Dev import Dev
from osbot_aws.apis.Lambda           import Lambda


class Test_lambda_api_gateway_simple_test(unittest.TestCase):
    def setUp(self):
        self.simple_test = Lambda('api_gateway.simple_test')

    def test_update_and_invoke(self):
        result = self.simple_test.update().invoke({'aa':'bb'})
        Dev.pprint(result)
        #assert result == 'API Gateway test'
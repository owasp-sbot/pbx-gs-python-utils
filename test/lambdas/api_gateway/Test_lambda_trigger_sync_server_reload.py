import unittest

from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_lambda_api_gateway_simple_test(unittest.TestCase):
    def setUp(self):
        self.target = Lambdas('api_gateway.trigger_server_reload')

    def test_update_and_invoke(self):
        result = self.target.update_with_src().invoke({})
        Dev.pprint(result)
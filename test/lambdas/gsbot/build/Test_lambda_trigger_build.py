import unittest

from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_lambda_trigger_build(unittest.TestCase):
    def setUp(self):
        self.hello_world = Lambdas('gsbot.build.trigger_build')

    def test_update_and_invoke(self):
        result = self.hello_world.update().invoke()
        Dev.pprint(result)
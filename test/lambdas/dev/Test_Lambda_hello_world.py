import unittest

from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Lambda_hello_world(unittest.TestCase):
    def setUp(self):
        self.hello_world = Lambdas('dev.hello_world')

    def test_update_and_invoke(self):
        payload ={ "name" : 'world'}
        result = self.hello_world.update().invoke(payload)
        assert result == 'hello world'
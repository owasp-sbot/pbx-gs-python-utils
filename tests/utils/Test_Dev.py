from unittest import TestCase

from utils.Dev import Dev


class Test_Dev(TestCase):

    def test_pprint(self):
        assert Dev.pprint('aaa')     == 'aaa'
        assert Dev.pprint('aaa',123) == ('aaa',123)

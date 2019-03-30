import re

from utils.Misc import Misc


class Assert:
    def __init__(self ,target):
        self.target = target


    def is_class(self, name):
        assert Misc.class_name(self.target) in name

    def contains(self, text):
        assert text in self.target

    def is_bigger_than(self, value):
        if type(self.target) is list:
            list_len = len(self.target)
            assert  list_len > value   , "array with len {0} was not bigger than {1}".format(list_len, value)
        else:
            assert self.target > value , "value {0} was not bigger than {1}".format(self.target, value)
        return self

    def is_smaller_than(self, value):
        if type(self.target) is list:
            list_len = len(self.target)
            assert  list_len < value   , "array with len {0} was not smaller than {1}".format(list_len, value)
        else:
            assert self.target < value , "value {0} was not smaller than {1}".format(self.target, value)
        return self

    def is_equal(self, to):
        assert self.target == to

    def match_regex(self, regex):
        assert re.compile(regex).match(self.target) is not None

    def size_is(self, to):
        assert len(self.target) == to

    def regex_not_match(self,regex):
        assert re.compile(regex).match(self.target) is None

import re

from utils.Misc import Misc


class Assert:
    def __init__(self ,target):
        self.target = target


    def is_class(self, name):
        assert Misc.class_name(self.target) in name

    def contains(self, text):
        assert text in self.target

    def is_equal(self, to):
        assert self.target == to

    def match_regex(self, regex):
        assert re.compile(regex).match(self.target) is not None

    def regex_not_match(self,regex):
        assert re.compile(regex).match(self.target) is None

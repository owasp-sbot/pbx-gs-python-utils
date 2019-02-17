from utils.Dev import Dev
from utils.Misc import Misc


class Test_Misc:

    def test_random_filename(self):
        result = Misc.random_filename()
        assert len(result) is 14
        assert ".tmp" in result
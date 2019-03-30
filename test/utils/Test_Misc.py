from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc


class Test_Misc:

    def test_random_filename(self):
        result = Misc.random_filename()
        assert len(result) is 14
        assert ".tmp" in result

    def test_exists(self):
        assert Files.exists(Files.current_folder()) is True
        assert Files.exists('aaaa_bbb_ccc'        ) is False
        assert Files.exists(None                  ) is False

    def test_is_number(self):
        assert Misc.is_number(123   ) is True
        assert Misc.is_number('123' ) is True
        assert Misc.is_number('abc' ) is False
        assert Misc.is_number(None  ) is False
        assert Misc.is_number([]    ) is False

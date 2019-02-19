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
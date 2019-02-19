import json
from unittest import TestCase

from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc
from utils.Zip_Folder import Zip_Folder


class Test_Zip_Folder(TestCase):

    def test__using_with__no_params(self):
        with Zip_Folder() as (zip_file):
            assert zip_file is None

    def test__using_with_params(self):
        target_folder = Files.current_folder()
        with Zip_Folder(target_folder) as (zip_file):
            assert Files.exists(zip_file) is True
        assert Files.exists(zip_file) is False




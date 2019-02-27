import json
from unittest import TestCase

from utils.Dev import Dev
from utils.Files import Files
from utils.Misc import Misc
from utils.Unzip_File import Unzip_File
from utils.Zip_Folder import Zip_Folder


class Test_Unzip_File(TestCase):

    def test__using_with__no_params(self):
        with Unzip_File() as (temp_Folder):
            assert temp_Folder is None

    def test__using_with_valid_zip_no_target_folder(self):
        test_zip = Files.current_folder()
        with Zip_Folder(test_zip) as (zip_file):
            with Unzip_File(zip_file,None,True) as temp_folder:
                assert Files.exists(temp_folder) is True
        assert Files.exists(temp_folder) is False

    def test__using_with_valid_zip_and_target_folder(self):
        test_zip      = Files.current_folder()
        target_folder = '/tmp/unzip_test'
        with Zip_Folder(test_zip) as (zip_file):
            with Unzip_File(zip_file,target_folder,True) as temp_folder:
                assert Files.exists(temp_folder) is True
        assert Files.exists(temp_folder) is False




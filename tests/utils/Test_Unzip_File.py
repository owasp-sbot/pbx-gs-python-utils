import json
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.Unzip_File import Unzip_File
from pbx_gs_python_utils.utils.Zip_Folder import Zip_Folder


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




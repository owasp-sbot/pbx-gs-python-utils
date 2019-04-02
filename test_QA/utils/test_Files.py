import sys
from unittest import TestCase

sys.path.append('..')

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Temp_File import Temp_File


class test_Files(TestCase):

    def test_zip_files(self):
        target_file = '/tmp/test_zip.zip'
        Files.delete(target_file)
        assert Files.exists(target_file) is False
        Dev.pprint(Files.zip_files('..','*.py','/tmp/test_zip.zip'))
        assert Files.exists(target_file) is True
        Files.delete(target_file)
        assert Files.exists(target_file) is False

    # def test_zip_files_from_two_folders(self):
    #     Dev.pprint(Files.zip_files_from_two_folders('../../libs/pbx-gs-python-utils/src/', '**/*File*.py','..', '**/*ELK*.py', '/tmp/test_zip.zip'))
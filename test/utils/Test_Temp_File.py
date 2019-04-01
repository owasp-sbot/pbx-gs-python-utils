
from unittest import TestCase
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Temp_File import Temp_File


class Test_Temp_File(TestCase):

    def test__init__(self):
        temp_file = Temp_File()
        assert Files.exists    (temp_file.tmp_folder)
        assert Files.not_exists(temp_file.tmp_file)
        assert Files.not_exists(temp_file.file_path)
        assert temp_file.tmp_folder in temp_file.file_path
        assert '/' == temp_file.file_path.replace(temp_file.tmp_folder,'').replace(temp_file.tmp_file,'')

    def test__using_with__no_params(self):
        with Temp_File() as temp:
            assert Files.file_extension(temp.file_path) == '.tmp'
            assert Files.exists  (temp.file_path)
            assert Files.contents(temp.file_path) == '...'
        assert Files.not_exists(temp.file_path)

        with Temp_File('abc','txt') as temp:
            assert Files.file_extension(temp.file_path) == '.txt'
            assert Files.exists  (temp.file_path)
            assert Files.contents(temp.file_path) == 'abc'
        assert Files.not_exists(temp.file_path)

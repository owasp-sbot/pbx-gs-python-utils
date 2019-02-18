

from unittest import TestCase

from utils.Dev      import Dev
from utils.Files  import Files


class Test_Files(TestCase):

    def test_folder_create(self):
        tmp_folder = '_tmp_folder'
        assert Files.folder_exists(tmp_folder) is False
        assert Files.folder_create(tmp_folder) == tmp_folder
        assert Files.folder_create(tmp_folder) == tmp_folder
        assert Files.folder_exists(tmp_folder) is True
        assert Files.folder_delete_all(tmp_folder) is True

    def test_file_extension(self):
        assert Files.file_extension('/path/to/somefile.ext') == '.ext'
        assert Files.file_extension('/path/to/somefile.'   ) == '.'
        assert Files.file_extension('/path/to/somefile..'  ) == '.'
        assert Files.file_extension('/path/to/somefile'    ) == ''
        assert Files.file_extension('/a/b.c/d'             ) == ''
        assert Files.file_extension('/a/b.c/.git'          ) == ''
        assert Files.file_extension('/a/b.c/a.git'         ) == '.git'
        assert Files.file_extension('/a/b.c/a.git.abc'     ) == '.abc'
        assert Files.file_extension(None)                    == ''

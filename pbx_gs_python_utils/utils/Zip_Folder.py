import tempfile

from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Misc import Misc


class Zip_Folder():
    def __init__(self, target_folder=None,delete_zip_file=True):
        self.target_folder   = target_folder
        self.zip_file        = None
        self.delete_zip_file = delete_zip_file

    def __enter__(self):
        if Files.exists(self.target_folder):
            self.zip_file = Files.zip_folder(self.target_folder)
        return self.zip_file

    def __exit__(self, type, value, traceback):
        if Files.exists(self.zip_file) and self.delete_zip_file:
            Files.delete(self.zip_file)
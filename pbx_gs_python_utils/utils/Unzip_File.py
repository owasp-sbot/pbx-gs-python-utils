import tempfile

from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Misc import Misc


class Unzip_File():
    def __init__(self, zip_file=None, target_folder=None,delete_target_folder=False):
        self.target_folder          = target_folder
        self.zip_file               = zip_file
        self.delete_target_folder   = delete_target_folder

    def __enter__(self):
        if Files.exists(self.zip_file):
            if self.target_folder is None: self.target_folder = Files.temp_folder("unzipped_")
            return Files.unzip_file(self.zip_file, self.target_folder)
        return None

    def __exit__(self, type, value, traceback):
        if Files.exists(self.target_folder) and self.delete_target_folder:
            Files.folder_delete_all(self.target_folder)
            print("\n\ndeleting", self.target_folder)
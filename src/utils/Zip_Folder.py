import tempfile

from utils.Files import Files
from utils.Misc import Misc


class Zip_Folder():
    def __init__(self, target_folder=None):
        self.target_folder = target_folder
        self.zip_file      = None

    def __enter__(self):
        if Files.exists(self.target_folder):
            self.zip_file = Files.zip_folder(self.target_folder)
        return self.zip_file

    def __exit__(self, type, value, traceback):
        if Files.exists(self.zip_file):
            Files.delete(self.zip_file)
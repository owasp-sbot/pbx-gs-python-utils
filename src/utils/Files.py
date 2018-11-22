import gzip
import os
import glob
import shutil
import tempfile
from   os.path import abspath, join


class Files:
    @staticmethod
    def contents(path):
        with open(path, "rt") as file:
            return file.read()

    @staticmethod
    def contents_gz(path):
        with gzip.open(path, "rt") as file:
            return file.read()

    @staticmethod
    def delete(path):
        if Files.exists(path):
            os.remove(path)
        return Files.exists(path) is False

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def find(path_pattern):
        return glob.glob(path_pattern)

    @staticmethod
    def file_name(path):
        return os.path.basename(path)

    @staticmethod
    def path_combine(path1, path2):
        return abspath(join(path1, path2))

    @staticmethod
    def lines_gz(path):
        with gzip.open(path, "rt") as file:
            for line in file:
                yield line

    @staticmethod
    def not_exists(path):
        return os.path.exists(path) is False

    @staticmethod
    def temp_file(extension = '.tmp'):
        (fd, tmp_file) = tempfile.mkstemp(extension)
        return '/tmp/{0}'.format(os.path.basename(tmp_file))

    @staticmethod
    def write(path,contents):
        with open(path, "w") as file:
            return file.write(contents)

    @staticmethod
    def zip_folder(root_dir):
        return shutil.make_archive(root_dir, "zip", root_dir)
    # @staticmethod
    # def save_string(file_Path,data):
    #     with open(file_Path, "w") as f:
    #         f.write(data)
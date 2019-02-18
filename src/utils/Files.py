import errno
import gzip
import os
import glob
import shutil
import tempfile
from   os.path import abspath, join


class Files:
    @staticmethod
    def copy(source, destination):
        parent_folder = Files.folder_name(destination)
        Files.folder_create(parent_folder)                      # ensure targer folder exists
        return shutil.copy(source, destination)

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
    def file_extension(path):
        if path:
            return os.path.splitext(path)[1]
        return ''

    @staticmethod
    def folder_exists(path):          # add check to see if it is a folder
        return Files.exists(path)

    @staticmethod
    def folder_create(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        if Files.folder_exists(path):
            return path
        return None

    @staticmethod
    def folder_delete_all(path):                # this will remove recursively
        shutil.rmtree(path)
        return Files.exists(path) is False

    @staticmethod
    def folder_name(path):
        return os.path.dirname(path)

    @staticmethod
    def path_combine(path1, path2):
        return abspath(join(path1, path2))

    @staticmethod
    def lines(path):
        with open(path, "rt") as file:
            for line in file:
                yield line

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
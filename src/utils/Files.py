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
    def current_folder():
        return Files.path_combine(".","")
    @staticmethod
    def delete(path):
        if Files.exists(path):
            os.remove(path)
        return Files.exists(path) is False

    @staticmethod
    def exists(path):
        if path:
            return os.path.exists(path)
        return False

    @staticmethod
    def find(path_pattern):
        return glob.glob(path_pattern, recursive=True)

    @staticmethod
    def files(path):
        search_path = Files.path_combine(path,'**/*.*')
        return Files.find(search_path)

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
    def parent_folder(path):
        return os.path.dirname(path)

    @staticmethod
    def parent_folder_combine(file, path):
        return Files.path_combine(os.path.dirname(file),path)

    @staticmethod
    def temp_file(extension = '.tmp'):
        (fd, tmp_file) = tempfile.mkstemp(extension)
        return tmp_file
        #return '/tmp/{0}'.format(os.path.basename(tmp_file))

    @staticmethod
    def temp_filename(extension='.tmp'):
        if len(extension) >0 and extension[0] !='.' :           # make sure the extension starts with a dot
            extension = '.' + extension
        return Files.file_name(Files.temp_file(extension))

    @staticmethod
    def temp_folder(prefix=None, suffix=None,parent_folder=None):
        return tempfile.mkdtemp(suffix, prefix, parent_folder)

    @staticmethod
    def write(path,contents):
        with open(path, "w") as file:
            return file.write(contents)

    @staticmethod
    def zip_folder(root_dir):
        return shutil.make_archive(root_dir, "zip", root_dir)

    @staticmethod
    def unzip_file(zip_file, target_folder):
        shutil.unpack_archive(zip_file, extract_dir=target_folder)
        return target_folder

        # @staticmethod
    # def save_string(file_Path,data):
    #     with open(file_Path, "w") as f:
    #         f.write(data)
import errno
import gzip
import os
import glob
import shutil
import tempfile
import zipfile
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
        if Files.folder_exists(path):
            shutil.rmtree(path)
            return Files.exists(path) is False
        return True

    @staticmethod
    def folder_name(path):
        return os.path.dirname(path)

    def find(path_pattern):
        return glob.glob(path_pattern)

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
        if len(extension) > 0 and extension[0] != '.':  # make sure the extension starts with a dot
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

    @staticmethod
    def zip_files(base_folder, file_pattern, target_file):
        if file_pattern and target_file and target_file:
            base_folder  = abspath(base_folder)
            file_pattern = Files.path_combine(base_folder, file_pattern)


            file_list = glob.glob(file_pattern)

            if len(file_list):                                                  # if there were files found
                with zipfile.ZipFile(target_file,'w') as zip:
                    for file_name in file_list:
                        zip_file_path = file_name.replace(base_folder,'')
                        zip.write(file_name, zip_file_path)

                return target_file

    # Not sure about the method below
    @staticmethod
    def zip_files_from_two_folders(base_folder_1, file_pattern_1,base_folder_2, file_pattern_2, target_file):
        if base_folder_1 and file_pattern_1 and base_folder_2 and file_pattern_2 and target_file:
            base_folder_1  = abspath(base_folder_1)
            file_pattern_1 = Files.path_combine(base_folder_1, file_pattern_1)
            base_folder_2  = abspath(base_folder_2)
            file_pattern_2 = Files.path_combine(base_folder_2, file_pattern_2)

            file_list_1 =  glob.glob(file_pattern_1)
            file_list_2 =  glob.glob(file_pattern_2)

            file_list = {}
            for file in file_list_1:
                file_list[file] = file.replace(base_folder_1,'')
            for file in file_list_2:
                file_list[file] = file.replace(base_folder_2,'')
            if len(set(file_list)) >0:

                with zipfile.ZipFile(target_file,'w') as zip:
                    for file_path,zip_file_path in file_list.items():
                        zip.write(file_path, zip_file_path)

                return target_file

            return len(set(file_list))
from gsuite.GSuite import GSuite
from utils.Dev import Dev


class GDrive:

    def __init__(self):
        self.files = GSuite().drive_v3().files()

    def execute(self, command):
        try:
            return command.execute()
        except Exception as error:
            Dev.pprint(error)                   # add better error handling log capture
            return None

    def file_export(self, file_Id):
        return self.files.export(fileId=file_Id, mimeType='application/pdf').execute()

    def file_metadata(self, file_Id, fields = "id,name"):
        return self.execute(self.files.get(fileId = file_Id, fields=fields))

    def file_metadata_update(self, file_Id, changes):
        return self.files.update(fileId=file_Id, body=changes).execute()

    def file_delete(self, file_Id):
        self.files.delete(fileId= file_Id).execute()

    def files(self, size):
        results = self.files.list(pageSize=size, fields="files(id,name)").execute()
        return results.get('files', [])

    def find_by_name(self, name):
        results = self.execute(self.files.list(q="name = '{0}'".format(name)))  # , fields="files(id,name)"))
        if len(results.get('files')) > 0:
            return results.get('files').pop()
        return None

    def find_by_mime_type(self, mime_type):
        results = self.execute(self.files.list(q="mimeType = '{0}'".format(mime_type), fields="files(id,name)"))
        return results.get('files', [])

    def set_file_title(self, file_id, new_title):
        return self.file_metadata_update(file_id, {"name" : new_title })

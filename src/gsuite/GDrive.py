from __future__ import print_function

from gsuite.GSuite import GSuite



class GDrive:

    def __init__(self):
        self.service = GSuite().drive_v3()

    def files(self, size):
        service = self.service
        results = service.files().list(pageSize=size, fields="files(id,name)").execute()
        return results.get('files', [])
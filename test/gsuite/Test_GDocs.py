from unittest        import TestCase
from gsuite.GDrive   import GDrive
from utils.Dev import Dev


class Test_GDrive(TestCase):
    def setUp(self):
        self.gdocs = GDrive()

    def test_ctor(self):
        service = self.gdocs.service
        assert service._baseUrl == 'https://www.googleapis.com/drive/v3/'

    def test_files(self):
        files = self.gdocs.files(4)
        for item in files:
            print('{0:22} - {1}'.format(item['name'], item['id']))



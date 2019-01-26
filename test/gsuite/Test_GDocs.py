from unittest        import TestCase
from gsuite.GDrive   import GDrive
from utils.Dev import Dev


class Test_GDrive(TestCase):
    def setUp(self):
        self.gdocs = GDrive()

    def test_ctor(self):
        service = self.gdocs.service
        assert service._baseUrl == 'https://www.googleapis.com/drive/v3/'

    def test_file_export(self):
        id = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'   # test document
        id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'   # test slides
        pdf_data = self.gdocs.file_export(id)

        with open('./test.pdf', "wb") as fh:
            fh.write(pdf_data)
            #fh.write(base64.decodebytes(pdf_data.encode()))
        #Dev.pprint(result)

    def test_file_metadata(self):
        id      = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'        # test document
        result  = self.gdocs.file_metadata(id)
        Dev.pprint(result)

    def test_files(self):
        files = self.gdocs.files(4)
        for item in files:
            print('{0:22} - {1}'.format(item['name'], item['id']))



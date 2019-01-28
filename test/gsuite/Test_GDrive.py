from unittest        import TestCase
from gsuite.GDrive   import GDrive
from utils.Dev import Dev


class Test_GDrive(TestCase):
    def setUp(self):
        self.gdrive = GDrive()

    def test_ctor(self):
        service = self.gdrive.service
        assert service._baseUrl == 'https://www.googleapis.com/drive/v3/'

    def test_file_find_by_name(self):
        name   = 'GSlides API tests'
        assert self.gdrive.find_by_name(name).get('name') == name
        assert self.gdrive.find_by_name('aaaa') is None

    def test_file_export(self):
        id = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'   # test document
        id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'   # test slides
        file_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        pdf_data = self.gdrive.file_export(id)

        with open('./test.pdf', "wb") as fh:
            fh.write(pdf_data)
            #fh.write(base64.decodebytes(pdf_data.encode()))
        #Dev.pprint(result)

    def test_file_metadata(self):
        file_id = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'            # test document
        result  = self.gdrive.file_metadata(file_id)
        Dev.pprint(result)

    def test_file_metadata_update(self):
        file_id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'            # test spreadsheet
        metadata = self.gdrive.file_metadata(file_id)
        Dev.pprint(metadata)
        changes =  self.gdrive.set_file_title(file_id,'GSlides API tests')
        Dev.pprint(changes)

    def test_files(self):
        files = self.gdrive.files(4)
        for item in files:
            print('{0:22} - {1}'.format(item['name'], item['id']))

    def testfiles_with_mime_type(self):
        mime_type_presentations = 'application/vnd.google-apps.presentation'
        files = self.gdrive.find_by_mime_type(mime_type_presentations)

        assert len(files) > 0



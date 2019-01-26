from unittest        import TestCase

from gsuite.GDrive    import GDrive
from gsuite.GSlides   import GSlides
from utils.Dev import Dev


class Test_GDrive(TestCase):
    def setUp(self):
        self.gslides = GSlides()
        self.gdrive  = GDrive()
        self.test_id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'

    def test_ctor(self):
        service = self.gslides.service
        assert service._baseUrl == 'https://slides.googleapis.com/'

    def test_all_presentations(self):
        result = self.gslides.all_presentations()
        assert len(result) > 0

    def test_presentation_get(self):
        presentation_id = self.gslides.presentation_create('created via Unit tests')
        result = self.gslides.presentation(presentation_id)

        assert set(result) == { 'layouts'       , 'locale'    , 'masters', 'notesMaster', 'pageSize',
                                'presentationId', 'revisionId', 'slides' , 'title'                  }

        assert result.get('title') == 'created via Unit tests'

        self.gdrive.file_delete(presentation_id)
        assert self.gslides.presentation(presentation_id) is None

    def test_presentation_create(self):
        presentation_id = self.gslides.presentation_create('created via Unit tests')
        Dev.pprint(presentation_id)

    def test_slide_elements(self):
        elements = self.gslides.slide_elements(self.test_id, 1)
        elements = self.gslides.slide_elements(self.test_id, 2)
        #elements = self.gslides.slide_elements(self.test_id, 3)
        Dev.pprint(elements)

    def test_slides_get(self):
        slides = self.gslides.slides_get(self.test_id)
        assert len(slides) > 0

        for i, slide in enumerate(slides):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))
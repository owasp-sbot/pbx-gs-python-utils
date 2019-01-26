from gsuite.GDrive import GDrive
from gsuite.GSuite import GSuite

class GSlides:

    def __init__(self):
        self.presentations = GSuite().slides_v1().presentations()
        self.gdrive        = GDrive()

    def all_presentations(self):
        mime_type_presentations = 'application/vnd.google-apps.presentation'
        return self.gdrive.find_by_mime_type(mime_type_presentations)

    def presentation_create(self, title):
        body = { 'title': title }
        presentation = self.presentations.create(body=body).execute()
        return presentation.get('presentationId')

    def presentation_get(self,presentation_id):
        try:
            return self.presentations.get(presentationId = presentation_id).execute()
        except:
            return None

    def slide_elements(self, presentation_id,page):
        page -= 1                                             # so that we can use page 1 or 2, instead of page 0 or 1
        slides = self.slides_get(presentation_id)
        if page < len(slides):
            return slides[page].get('pageElements')
        return []

    def slides_get(self, presentation_id):
        presentation = self.presentation_get(presentation_id)
        if presentation:
            return presentation.get('slides')
        return []


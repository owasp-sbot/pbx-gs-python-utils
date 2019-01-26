from gsuite.GDrive import GDrive
from gsuite.GSuite import GSuite
from utils.Dev import Dev


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

    def slide_elements(self, presentation_id, page_number):
        slides = self.slides(presentation_id)
        page   = slides[page_number]
        if page:
            return page.get('pageElements')
        return []

    def slides(self, presentation_id):
        presentation = self.presentation_get(presentation_id)
        if presentation:
            return presentation.get('slides')
        return []


    def set_element_text(self, file_id, element_id, text):

        body = { 'requests' : [    {   'deleteText' : { 'objectId'      : element_id         ,
                                                        'textRange'     : { 'type': 'ALL' }}},
                                   {
                                       'insertText': { 'objectId'      : element_id          ,
                                                       'insertionIndex': 0                   ,
                                                       'text'          : text             }}]}

        return self.gdrive.execute(self.presentations.batchUpdate(presentationId=file_id, body=body))
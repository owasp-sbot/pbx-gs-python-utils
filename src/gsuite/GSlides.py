from gsuite.GDrive import GDrive
from gsuite.GSuite import GSuite
from utils.Dev import Dev
from utils.Misc import Misc


class GSlides:

    def __init__(self):
        self.presentations = GSuite().slides_v1().presentations()
        self.gdrive        = GDrive()

    # misc utils

    def batch_update(self, file_id, requests):
        body = {'requests': requests  }
        return self.execute(self.presentations.batchUpdate(presentationId=file_id, body=body))

    def execute(self,command):
        return self.gdrive.execute(command)

    def execute_requests(self, file_id, requests):
        return self.batch_update(file_id, requests)


    def random_id(self, prefix):
        return Misc.random_string_and_numbers(6, prefix + "_")


    def all_presentations(self):
        mime_type_presentations = 'application/vnd.google-apps.presentation'
        return self.gdrive.find_by_mime_type(mime_type_presentations)


    # Elements
    def element_create_image(self, file_id, page_id, image_url, x_pos=200, y_pos=200, width=100, height=100):
        requests = [ {  "createImage": {
                        "url"        : image_url,
                        "elementProperties": {
                            "pageObjectId": page_id,
                            "size": { "width" : { "magnitude": width, "unit": "PT" },
                                      "height": { "magnitude": height,"unit": "PT" }},
                            "transform": { "scaleX": 1, "scaleY": 1, "translateX": x_pos, "translateY": y_pos, "unit": "PT" }}}}]
        result = self.batch_update(file_id, requests)
        return result.get('replies')[0].get('createImage').get('objectId')

    def element_create_table(self, file_id, slide_id, rows = 3, cols = 3):
        requests = [   { "createTable": { "elementProperties": { "pageObjectId": slide_id  },
                                          "rows"             : rows                         ,
                                          "columns"          : cols                       }}]
        result = self.batch_update(file_id, requests)
        return result.get('replies')[0].get('createTable').get('objectId')

    def element_create_text(self,file_id, page_id, text = "Text...", x_pos=200, y_pos=200, width=100, height=100):
        element_id = self.random_id('Textbox')
        requests = [ { 'createShape': { 'objectId': element_id,
                                        'shapeType': 'TEXT_BOX',
                                        'elementProperties': {
                                            'pageObjectId': page_id,
                                            'size'        : { 'height': { 'magnitude': height, 'unit': 'PT'},
                                                              'width' : { 'magnitude': width , 'unit': 'PT'}},
                                            'transform'   : { 'scaleX': 1, 'scaleY': 1, 'translateX': x_pos, 'translateY': y_pos, 'unit': 'PT' }}}},
                    { 'insertText': { 'objectId': element_id, 'insertionIndex': 0, 'text': text                                                  }}]

        result = self.batch_update(file_id, requests)
        return result.get('replies')[0].get('createShape').get('objectId')

    def element_create_shape(self,file_id, page_id, shape_type, x_pos=200, y_pos=200, width=100, height=100):
        requests = [ { 'createShape': { 'shapeType': shape_type,
                                        'elementProperties': {
                                            'pageObjectId': page_id,
                                            'size'        : { 'height': { 'magnitude': height, 'unit': 'PT'},
                                                              'width' : { 'magnitude': width , 'unit': 'PT'}},
                                            'transform'   : { 'scaleX': 1, 'scaleY': 1, 'translateX': x_pos, 'translateY': y_pos, 'unit': 'PT' }}}}]

        result = self.batch_update(file_id, requests)
        if result:
            return result.get('replies')[0].get('createShape').get('objectId')

    def element_delete(self, file_id, element_id):
        requests = [ {  'deleteObject' : { 'objectId': element_id } } ]
        return self.batch_update(file_id, requests)

    def element_set_text(self, file_id, element_id, text):

        requests =  [    {   'deleteText' : { 'objectId'      : element_id         ,
                                              'textRange'     : { 'type': 'ALL' }}},
                         {
                             'insertText': { 'objectId'      : element_id          ,
                                             'insertionIndex': 0                   ,
                                             'text'          : text             }}]

        return self.batch_update(file_id, requests)

    def element_set_text_style(self, file_id, shape_id,style, fields):
        requests = [{'updateTextStyle': { 'objectId': shape_id  ,
                                          'style'   : style     ,
                                          'fields'  : fields  }}]
        return self.batch_update(file_id, requests)

    def element_set_shape_properties(self, file_id, shape_id,properties , fields=None):
        if fields is None:
            fields = ",".join(list(set(properties)))
        requests = [{'updateShapeProperties': { 'objectId'         : shape_id     ,
                                                'shapeProperties'  : properties   ,
                                                'fields'           : fields     }}]
        return self.batch_update(file_id, requests)

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

    def slide_elements_indexed_by_id(self, presentation_id, page_number):
        elements = {}
        for element in self.slide_elements(presentation_id,page_number):
            elements[element.get('objectId')] = element
        return elements

    def slides(self, presentation_id):
        presentation = self.presentation_get(presentation_id)
        if presentation:
            return presentation.get('slides')
        return []



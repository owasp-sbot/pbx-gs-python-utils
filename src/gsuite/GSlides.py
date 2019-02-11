from gsuite.GDrive import GDrive
from gsuite.GSuite import GSuite
from utils.Dev import Dev
from utils.Misc import Misc


class GSlides:

    def __init__(self, gsuite_secret_id=None):
        self.presentations = GSuite(gsuite_secret_id).slides_v1().presentations()
        self.gdrive        = GDrive(gsuite_secret_id)

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

    def element_set_table_text_request(self, file_id, table_id, row, col, text):
        return     [{ "deleteText": {   "objectId"      : table_id,
                                        "cellLocation"  : {  "rowIndex": row, "columnIndex": col   },
                                        "textRange"     : {"type": "ALL"                         }}},
                    { "insertText": {   "objectId"      : table_id,
                                        "cellLocation"  : {  "rowIndex": row, "columnIndex": col   },
                                        "text"          : text,
                                        "insertionIndex": 0                                       }}]
    def element_set_table_text(self, file_id, table_id, row, col, text):
        requests = self.element_set_table_text_request(file_id, table_id, row, col, text)

        self.execute_requests(file_id,requests)

    def element_set_text_request(self, file_id, element_id, text):
        return [ {   'deleteText' : { 'objectId'      : element_id         ,
                                      'textRange'     : { 'type': 'ALL' }}},
                 {
                     'insertText': { 'objectId'      : element_id          ,
                                     'insertionIndex': 0                   ,
                                     'text'          : text              }}]
    def element_set_text(self, file_id, element_id, text):

        requests =  self.element_set_text_request(file_id, element_id, text)

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

    def presentation_copy(self, file_id, title):
        body  = { 'name': title }
        result = self.execute(self.gdrive.files.copy(fileId = file_id, body=body))
        return result.get('id')

    def presentation_metadata(self,presentation_id):
        try:
            return self.presentations.get(presentationId = presentation_id).execute()
        except:
            return None

    def slide_delete(self,presentation_id, slide_id):
        requests =   [ { "deleteObject": { "objectId" : slide_id}} ]
        return self.execute_requests(presentation_id, requests)

    def slide_copy(self,presentation_id, slide_id, new_slide_id, objects_ids = {}):
        requests =   [ { "duplicateObject": {
                                                "objectId" : slide_id,
                                                "objectIds": objects_ids}} ]
        requests[0]['duplicateObject']['objectIds'][slide_id] = new_slide_id
        return self.execute_requests(presentation_id, requests)

    def slide_create(self, presentation_id, insert_at=1, layout='TITLE', new_slide_id=None):
        requests =   [ { "createSlide": {       "objectId"      : new_slide_id,
                                                'insertionIndex': insert_at,
                                                'slideLayoutReference': { 'predefinedLayout': layout } }}]
        result = self.execute_requests(presentation_id, requests)
        return result.get('replies')[0].get('createSlide').get('objectId')


    def slide_move_to_pos_request(self, presentation_id, slide_id, pos):
        return [{ "updateSlidesPosition": { "slideObjectIds": [ slide_id],
                                            "insertionIndex": pos }}]
    def slide_move_to_pos(self, presentation_id, slide_id, pos):
        requests = self.slide_move_to_pos_request(presentation_id, slide_id, pos)
        return self.execute_requests(presentation_id,requests)

    def slide_elements(self, presentation_id, page_number):
        slides = self.slides(presentation_id)
        page   = slides[page_number]
        if page:
            return page.get('pageElements')
        return []

    def slide_elements_via_id(self, presentation_id, slide_id):
        slides = self.slides_indexed_by_id(presentation_id)
        slide = slides.get(slide_id)
        if slide:
            return slide.get('pageElements')
        return []

    def slide_elements_via_id_indexed_by_id(self, presentation_id, slide_id):
        elements = {}
        for element in self.slide_elements_via_id(presentation_id,slide_id):
            elements[element.get('objectId')] = element
        return elements

    def slides(self, presentation_id):
        presentation = self.presentation_metadata(presentation_id)
        if presentation:
            return presentation.get('slides')
        return []

    def slides_indexed_by_id(self, presentation_id):
        presentation = self.presentation_metadata(presentation_id)
        slides = {}
        if presentation:
            for slide in presentation.get('slides'):
                slides[slide.get('objectId')] = slide
        return slides



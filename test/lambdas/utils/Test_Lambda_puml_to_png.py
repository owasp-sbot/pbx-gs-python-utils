import  unittest
from    utils.Dev              import Dev
from pbx_gs_python_utils.utils.Show_Img import Show_Img
from utils.aws.Lambdas import Lambdas


class Test_Lambda_dot_to_png(unittest.TestCase):
    def setUp(self):
        #upload_dependency('plantuml')
        #path_libs = '../_lambda_dependencies/plantuml'
        self.plant_to_png = Lambdas('utils.puml_to_png', memory =3008).delete().create() #,path_libs=path_libs)

    def test_update_invoke(self):
        puml = "@startuml \n aaa30->bbb12 \n @enduml"
        result = self.plant_to_png.update().invoke({"puml": puml})

        Dev.pprint(result)
        #Show_Img.from_svg_string(result['png_base64'])

    def test_just_invoke___more_complex_diagram(self):

        puml = """
@startuml
/'skinparam dpi 500 '/
:Main aaa Admin: as Admin
(Use the application) as (Use)

User -> (Start)
User --> (Use)
(Use) --> (b50011)

Admin ---> (Use)

note right of admin : This is an example.

note right of (Use)
  A note can also
  be on several lines
  very cool
end note

note "This note is connected\\nto several objects." as N2
(Start) .. N2
N2 .. (Use)
@enduml
"""
        result = self.plant_to_png.invoke({"puml": puml})
        Show_Img.from_svg_string(result['png_base64'])
import  unittest
from    utils.Dev              import Dev
from pbx_gs_python_utils.utils.Show_Img import Show_Img
from osbot_aws.apis.Lambda           import Lambda


class Test_Lambda_dot_to_png(unittest.TestCase):
    def setUp(self):
        self.dot_to_png = Lambda('utils.dot_to_png')

    def test_update_invoke(self):
        dot = """digraph G {\naaa -> bbb;\n}\n"""
        png = self.dot_to_png.update().invoke({"dot": dot})

        Dev.pprint(png)
        #Show_Img.from_svg_string(png)

    def test_update_invoke__small_image(self):
        dot = """digraph G {\naaa -> bbb;\n}\n"""
        png = self.dot_to_png.update().invoke({"dot": dot, "width": 25})  # see pic SciView which should have less quality

        Show_Img.from_svg_string(png)

    def test_update_invoke__trigger_error(self):
        dot = """digraph G {\naaaa-aaa-aaa-a>--asd@£-ad;\n}\n"""
        result = self.dot_to_png.update().invoke({"dot":  dot, "channel": "DDKUZTK6X"})
        Dev.pprint(result)
import  os
import  tempfile
import  pydot
import  unittest
from    utils.Dev           import Dev
from pbx_gs_python_utils.utils.Files import Files
from utils.aws.Lambdas import Lambdas


class Test_Lambda_dot_to_svg(unittest.TestCase):
    def setUp(self):
        self.dot_to_svg = Lambdas('utils.dot_to_svg')

    def test_dot_round_trip(self):
        graph = pydot.Dot(graph_type='digraph')
        graph.add_edge(pydot.Edge("aaa", "bbb"))
        dot = graph.to_string()
        assert dot == """digraph G {\naaa -> bbb;\n}\n"""
        graph = pydot.graph_from_dot_data(dot).pop()
        assert graph.to_string() == dot

        (fd, tmp_file) = tempfile.mkstemp('dot)')
        graph.write_svg(tmp_file, prog='dot')
        assert os.path.exists(tmp_file)
        os.remove(tmp_file)


    def test_upload_and_invoke____simple_dot_file(self):

        # chars_1 = [100, 105, 103, 114, 97, 112, 104, 32, 71, 32, 123, 32, 98, 98, 32, 45, 62              , 32, 99, 99, 99, 32, 32, 125, 32]
        # chars_2 = [100, 105, 103, 114, 97, 112, 104, 32, 71, 32, 123, 32, 98, 98, 32, 45, 38, 103, 116, 59, 32, 99, 99, 99, 32, 32, 125, 32]
        #
        # string_1 = [chr(c) for c in chars_1]
        # string_2 = [chr(c) for c in chars_2]
        # Dev.print(string_1)
        # Dev.print(string_2)
        # return
        graph = pydot.Dot(graph_type='digraph')
        graph.add_edge(pydot.Edge("aaa","bbb"))
        params = { "dot" : graph.to_string()}

        params = { "dot" :  "digraph G { bb -> ccc  } "}
        result = self.dot_to_svg.upload_and_invoke(params)

        Dev.pprint(result)

    def test_invoke_simple____dot_file(self):
        graph = pydot.Dot(graph_type='digraph')
        graph.add_edge(pydot.Edge("aaa","bbb"))
        params = {"dot": graph.to_string(), "channel": "DDKUZTK6X"}
        result = self.dot_to_svg.update().invoke(params)
        #result = self.dot_to_svg.invoke({"dot": 'digraph {\na -> b[label="hi", decorate];\n}'})

        Dev.pprint(result)

    def test_invoke___jira_issues_dot_file(self):

        dot = Files.contents('../../../data/jira-test.dot')
        Dev.pprint(dot)
        params = { "dot": dot , "channel": "DDKUZTK6X"}
        svg = self.dot_to_svg.update().invoke(params)
        #how_Img.from_svg_string(svg)
        Dev.pprint(svg)

    def test_invoke_simple____bad_dot_code(self):
        dot = "asdasd-asd-asd>-<ASd£$%^sd"
        params = {"dot": dot, "channel": "DDKUZTK6X"}
        result = self.dot_to_svg.update().invoke(params)
        Dev.pprint(result)

    def test_invoke_simple____bad_dot_code_v2__now_fixed(self):
        dot_code = """digraph G {            
_node [style = "filled, rounded", shape = box, color = "#919191", fontcolor = white, fontsize = 14];
 h [label="Me hungry"]
 node [style = "filled, rounded", shape = diamond, color = "#919191", fontcolor = white, fontsize = 14];
 e [label="What to eat?"]
 node [style = "filled", shape = circle, color = "#ff0000", fontcolor = white, fontsize = 14];
 p1 [label="pork 1"]
 p2 [label="pork 2"]
 p3 [label="pork 3"]

 h -> e [dir="forward", label = "decisions, decisions"]

 edge [dir="forward", label = "this one"]
 e -> p1 
 e -> p2
 e -> p3
                       }  """

        params = {"dot": dot_code, "channel": "DDKUZTK6X"}
        result = self.dot_to_svg.update().invoke(params)

        assert len(result) > 100








    #handler = 'index.handle'
    #path_libs = '../_lambda_dependencies/phantomjs'
    # path_libs = '../_lambda_dependencies/requests'
    #_lambda = Lambdas('dev.node_phantom', handler=handler, runtime='nodejs8.10', path_libs=path_libs)
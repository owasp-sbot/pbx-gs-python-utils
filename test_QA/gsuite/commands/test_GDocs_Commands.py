from unittest import TestCase

from pbx_gs_python_utils.utils.aws.Lambdas      import load_dependency
load_dependency('gmail')

from pbx_gs_python_utils.gsuite.commands.GDocs_Commands import GDocs_Commands
from pbx_gs_python_utils.utils.Dev                      import Dev

class test_GDocs_Commands(TestCase):

    # def test_update_lambda(self):
    #     Lambdas('gs.lambda_gdocs').update_with_src()

    def test_list(self):
        params = []
        text,attachments = GDocs_Commands.list(None, None, params)
        assert ":point_right: Found" in text

    def test_pdf(self):
        params = ["1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI"]
        team_id = 'T7F3AUXGV'
        channel = 'GDL2EC3EE'
        result = GDocs_Commands.pdf(team_id, channel,params)
        Dev.pprint(result)
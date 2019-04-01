from unittest import TestCase

from pbx_gs_python_utils.lambdas.gs.lambda_gdocs import run
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Test_Lambda_lambda_gdocs(TestCase):
    def setUp(self):
        self.lambda_gdocs = Lambdas('pbx_gs_python_utils.lambdas.gs.lambda_gdocs', memory=3008)

    # def test_update(self):
    #     self.lambda_gdocs.update_with_lib()

    def test_invoke_directly(self):
        response = run({ 'data':{}},{})
        assert response == ( '*Here are the `GDocs_Commands` commands available:*',
                              [ { 'actions': [],
                                  'callback_id': '',
                                  'color': 'good',
                                  'fallback': None,
                                  'text': ' • list\n • pdf\n'}])

    def test_invoke___with_no_command(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': []})
        assert result == [ '*Here are the `GDocs_Commands` commands available:*',
                          [ { 'actions': [],
                              'callback_id': '',
                              'color': 'good',
                              'fallback': None,
                              'text': ' • list\n • pdf\n'}]]

    def test_pdf(self):
        self.lambda_gdocs.update_with_lib()
        result = self.lambda_gdocs.invoke({ 'data':{}, 'params':['pdf','1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI']})
        Dev.pprint(result)
        #assert result == [None,None]

    def test_version(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': ['version']})
        assert result == ['v0.21',[]]

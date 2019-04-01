from unittest import TestCase

from pbx_gs_python_utils.lambdas.gs.lambda_gdocs import run
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Test_Lambda_lambda_gdocs(TestCase):
    def setUp(self):
        self.lambda_gdocs = Lambdas('pbx_gs_python_utils.lambdas.gs.lambda_gdocs', memory=3008)

    #def test_update(self):
    #    self.lambda_gdocs.update_with_src()

    def test_invoke_directly(self):
        response = run({},{})
        Dev.pprint(response)

    def test_invoke(self):
        result = self.lambda_gdocs.update_with_src().invoke({ 'data':{}, 'params':['pdf','1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI']})
        Dev.pprint(result)
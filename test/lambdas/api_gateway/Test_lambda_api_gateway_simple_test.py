import unittest

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_aws.apis.Lambda           import Lambda


class Test_lambda_api_gateway_simple_test(unittest.TestCase):
    def setUp(self):
        self.simple_test = Lambda('api_gateway.trigger_sync_jira_sheets')

    def test_update_and_invoke(self):
        file_id = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        result = self.simple_test.update_with_src().invoke({'queryStringParameters':{'file_id':file_id}})
        message = Misc.json_load(result.get('body'))
        Dev.pprint(message)
        #assert result == 'API Gateway test'

    def test_update_and_invoke__action_diff(self):
        file_id = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        result = self.simple_test.update_with_src().invoke({'queryStringParameters':{'file_id':file_id, 'action':'diff'}})
        message = Misc.json_load(result.get('body'))
        Dev.pprint(message)

    def test_update_and_invoke__action_sync(self):
        file_id = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        result = self.simple_test.update_with_src().invoke({'queryStringParameters':{'file_id':file_id, 'action':'sync'}})
        message = Misc.json_load(result.get('body'))
        Dev.pprint(message)

    def test_just_update(self):
        self.simple_test.update_with_src()
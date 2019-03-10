import unittest

from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.Lambdas import Lambdas


class Test_lambda_api_gateway_simple_test(unittest.TestCase):
    def setUp(self):
        self.simple_test = Lambdas('api_gateway.trigger_sync_jira_sheets')

    def test_update_and_invoke(self):
        file_id = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        result = self.simple_test.update().invoke({'queryStringParameters':{'file_id':file_id}})
        message = Misc.json_load(result.get('body'))
        Dev.pprint(message)
        #assert result == 'API Gateway test'

    def test_update_and_invoke__action_diff(self):
        file_id = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        result = self.simple_test.update().invoke({'queryStringParameters':{'file_id':file_id, 'action':'diff'}})
        message = Misc.json_load(result.get('body'))
        Dev.pprint(message)
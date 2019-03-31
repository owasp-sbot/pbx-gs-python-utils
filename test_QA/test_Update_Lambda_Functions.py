import json
import sys
sys.path.append('..')
from unittest import TestCase
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers   import slack_message
from pbx_gs_python_utils.Update_Lambda_Functions import Update_Lambda_Functions

class test_Update_Lambda_Functions(TestCase):
    def setUp(self):
        self.update = Update_Lambda_Functions()

    def test_update_lambda_functions(self):
        Dev.pprint('in test_update_lambda_functions')
        result = self.update.update_lambda_functions()

        Dev.pprint(result)
        text = ":building_construction: pbx_gs_python_utils.update_lambda_functions:"
        attachments = [ { 'text': json.dumps(result,indent=4) , 'color':'good'}]
        slack_message(text,attachments,'GDL2EC3EE')  #gs-bot-tests
        #Dev.pprint(result)

    #
    # def test_healthcheck_gs_elastic_jira(self):
    #     Dev.pprint(self.update.healthcheck_gs_elastic_jira())


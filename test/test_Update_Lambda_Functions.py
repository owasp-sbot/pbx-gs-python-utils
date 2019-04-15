# import json
# import sys
# import unittest
#
# sys.path.append('..')
#
# from unittest import TestCase
# #from pbx_gs_python_utils.utils.Dev import Dev
# from pbx_gs_python_utils.utils.Lambdas_Helpers   import slack_message
# from pbx_gs_python_utils.Update_Lambda_Functions import Update_Lambda_Functions
#
# @unittest.skip("only use this for debugging")
# class test_Update_Lambda_Functions(TestCase):
#     def setUp(self):
#         self.update = Update_Lambda_Functions()
#
#     def test_update_lambda_functions(self):
#         print('\n\n')
#         slack_message(':zero: in test_update_lambda_functions',[],'GDL2EC3EE')
#         result      = self.update.update_lambda_functions()
#         text        = ":building_construction: pbx_gs_python_utils.update_lambda_functions:"
#         attachments = [ { 'text': json.dumps(result,indent=4) , 'color':'good'}]
#         slack_message(text,attachments,'GDL2EC3EE')  #gs-bot-tests
#         slack_message(':one: finished test_update_lambda_functions',[],'GDL2EC3EE')
#         print('\n\n')
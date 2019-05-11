# import sys
# sys.path.append('..')
#
# import json
#
# from pbx_gs_python_utils.utils.Dev              import Dev
# from pbx_gs_python_utils.utils.Lambdas_Helpers  import slack_message
# from osbot_aws.apis.Lambda           import Lambda
#
#
# class Update_Lambda_Functions:
#
#     def update_lambda_function(self, name):
#         try:
#             Lambda(name).update_with_lib()
#             return { 'status':'ok' , 'name': name}
#         except Exception as error:
#             return { 'status':'error' , 'name': name, 'details': '{0}'.format(error)}
#
#     def update_lambda_functions(self):
#         print('\n in update_lambda_functions ... \n')
#
#         targets = [
#                     'pbx_gs_python_utils.lambdas.gsbot.lambda_gs_bot',      # lambda_gs_bot     API_GS_Bot              GS_Bot_Commands
#                     'pbx_gs_python_utils.lambdas.gsbot.gsbot_gs_jira',      # gsbot_gs_jira     GS_Bot_                 Jira_Commands
#                     'pbx_gs_python_utils.lambdas.gsbot.gsbot_slack'  ,      # gsbot_slack       Slack_Commands_Helper
#
#                     'pbx_gs_python_utils.lambdas.gs.elastic_jira'    ,      # elastic_jira      GS_Bot_Jira
#
#                     'pbx_gs_python_utils.lambdas.utils.log_to_elk'   ,      # log_to_elk        Log_To_Elk
#                     'pbx_gs_python_utils.lambdas.utils.slack_message',      # slack_message     API_Slack
#
#                    ]
#         result = []
#         for target in targets:
#             result.append(self.update_lambda_function(target))
#
#         text = ":building_construction: *updated lambda functions* for `pbx_gs_python_utils`:"
#         attachments = [{'text': json.dumps(result, indent=4), 'color': 'good'}]
#         slack_message(text, attachments,'DDKUZTK6X','T7F3AUXGV')  # gs-bot-tests
#         Dev.pprint(result)
#
#         return result
#
#    # def healthcheck_gs_elastic_jira(self):
#    #     target = Lambda('gs.elastic_jira')
#    #     Dev.pprint(target.info())
#
#
# if __name__ == '__main__':
#     Update_Lambda_Functions().update_lambda_functions()
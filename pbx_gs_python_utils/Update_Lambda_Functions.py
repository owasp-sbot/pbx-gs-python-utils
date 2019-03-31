from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Update_Lambda_Functions:

    def update_lambda_function(self, name):
        try:
            Lambdas(name).update_with_lib()
            return { 'status':'ok' , 'name': name}
        except Exception as error:
            return { 'status':'error' , 'name': name, 'details': '{0}'.format(error)}

    def update_lambda_functions(self):

        targets = [
                    'pbx_gs_python_utils.lambdas.gsbot.lambda_gs_bot',      # lambda_gs_bot     API_GS_Bot GS_Bot_Commands
                    'pbx_gs_python_utils.lambdas.gsbot.gsbot_gs_jira',      # gsbot_gs_jira     GS_Bot_Jira_Commands
                    'pbx_gs_python_utils.lambdas.gsbot.gsbot_slack'  ,      # gsbot_slack       Slack_Commands_Helper
                    'pbx_gs_python_utils.lambdas.gs.elastic_jira'    ,      # elastic_jira      GS_Bot_Jira
                    'pbx_gs_python_utils.lambdas.utils.slack_message'       # slack_message     API_Slack

                   ]
        result = []
        for target in targets:
            result.append(self.update_lambda_function(target))
        return result

   # def healthcheck_gs_elastic_jira(self):
   #     target = Lambdas('gs.elastic_jira')
   #     Dev.pprint(target.info())
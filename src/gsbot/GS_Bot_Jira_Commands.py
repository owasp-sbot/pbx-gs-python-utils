# These are the methods to be called by Slack
from utils.Lambdas_Helpers import slack_message
from utils.aws.secrets import Secrets

class GS_Bot_Jira_Commands:

    @staticmethod
    def projects(team_id=None, channel=None, params=None):
        return 422222

    @staticmethod
    def invoke(team_id=None, channel=None, params=None):
        slack_message("in test invoke", [], channel, params)
        import requests
        data = Secrets('sync-server-ngrok').value_from_json_string()
        username = data.get('username')
        password = data.get('password')
        command = 'server/version'
        command = 'gsbot_jira/invoke/{"params":["projects"]}'
        url = "https://gs-jira.ngrok.io/{0}".format(command)
        result = requests.get(url, auth=(username, password)).text
        text = "....jira server invocation result: {0}".format(result)
        return slack_message(text,[],channel,params)

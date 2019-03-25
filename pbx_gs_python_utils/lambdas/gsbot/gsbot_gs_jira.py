from utils.aws.Lambdas import load_dependency
from utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


def run(event, context):
    data   = event.get('data')
    if data:
        load_dependency('requests')
        channel = data.get('channel')
        team_id = data.get('team_id')
        params  = event.get('params')
        from gs_jira.GS_Bot_Jira_Commands import GS_Bot_Jira_Commands
        Slack_Commands_Helper(GS_Bot_Jira_Commands).invoke(team_id, channel, params)

from utils.Lambdas_Helpers import log_to_elk
from utils.aws.Lambdas import load_dependency
from utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


def run(event, context):
    data   = event.get('data')
    if data:
        load_dependency('slack')
        channel = data.get('channel')
        team_id = data.get('team_id')
        params  = event.get('params')
        from gsbot.Slack_Commands import Slack_Commands
        Slack_Commands_Helper(Slack_Commands).invoke(team_id, channel, params)
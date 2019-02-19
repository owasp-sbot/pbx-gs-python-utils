from browser.Browser_Commands import Browser_Commands
from utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


def run(event, context):
    params  = event.get('params')
    data    = event.get('data')
    channel = None
    team_id = None
    if data:
        channel = data.get('channel')
        team_id = data.get('team_id')
    data,_ = Slack_Commands_Helper(Browser_Commands).invoke(team_id, channel, params)
    return data
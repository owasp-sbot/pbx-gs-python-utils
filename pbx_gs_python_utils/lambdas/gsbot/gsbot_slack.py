def run(event, context):
    from osbot_aws.apis.Lambda import load_dependency
    from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper

    data   = event.get('data')
    if data is not None:
        load_dependency('slack')
        channel = data.get('channel')
        team_id = data.get('team_id')
        params  = event.get('params')
        from pbx_gs_python_utils.gsbot.Slack_Commands import Slack_Commands
        return Slack_Commands_Helper(Slack_Commands).invoke(team_id, channel, params)
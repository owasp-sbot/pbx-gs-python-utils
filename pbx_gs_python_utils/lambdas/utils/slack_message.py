def run(event, context):
    from osbot_aws.apis.Lambda import load_dependency
    load_dependency('slack')

    from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
    
    channel     = event.get('channel'    )
    team_id     = event.get('team_id')
    text        = event.get('text'       )
    attachments = event.get('attachments')
    return API_Slack(channel = channel,team_id=team_id).send_message(text, attachments)

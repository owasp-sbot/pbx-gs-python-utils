def run(event, context):

    from pbx_gs_python_utils.utils.aws.Lambdas import load_dependency
    load_dependency('slack')

    from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
    
    channel     = event.get('channel'    )
    text        = event.get('text'       )
    attachments = event.get('attachments')
    return API_Slack(channel = channel).send_message(text, attachments)

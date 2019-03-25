from utils.slack.API_Slack import API_Slack

def run(event, context):
    channel     = event.get('channel'    )
    text        = event.get('text'       )
    attachments = event.get('attachments')
    return API_Slack(channel = channel).send_message(text, attachments)

from pbx_gs_python_utils.utils.Lambdas_Helpers  import slack_message, log_to_elk
from pbx_gs_python_utils.utils.aws.Lambdas      import load_dependency

def run(event, context):
    load_dependency("elastic-slack")
    try:
        log_to_elk("[elastic jira][event]: {0}".format(event))

        from pbx_gs_python_utils.gs.GS_Bot_Jira import GS_Bot_Jira                               # import class
        result = GS_Bot_Jira().handle_request(event)                         # invoke lambda main handler method

        log_to_elk("[elastic jira][result]: {0}".format(result))
        channel = event.get('channel')
        team_id = event.get('team_id')
        if result and channel:
            slack_message(result.get('text'), result.get('attachments'), channel, team_id)
        return result
    except Exception as error:
        log_to_elk("[elastic jira][Error]: {0}".format(error) , level='error')
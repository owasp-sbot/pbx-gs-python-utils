

from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_aws.apis.Lambda import Lambda


def run(event, context):
    team_id = 'T7F3AUXGV'
    channel = 'DDKUZTK6X'
    querystring = event.get('queryStringParameters')
    if querystring and querystring.get('file_id'):
        file_id = querystring.get('file_id')
        if querystring.get('action') == 'diff':
            payload = {"params": ["diff_sheet", file_id], "channel": "DDKUZTK6X", 'team_id': 'T7F3AUXGV'}
        elif querystring.get('action') == 'sync':
            payload = {"params": ["sync_sheet", file_id], "channel": "DDKUZTK6X", 'team_id': 'T7F3AUXGV'}
        else:
            payload  = {"params": [ "load_sheet",file_id], "channel": "DDKUZTK6X", 'team_id': 'T7F3AUXGV'}
        Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke(payload)
        text = ":point_right: [trigger_sync_jira_sheets] completed workflow for file_id: {0} , see channel {1} for more details".format(file_id,channel)
        status_code = 201
    else:
        text ="Error: file_id value not provided"
        status_code = 501

    slack_message(text, [], channel,team_id)


    return {
                'headers'        : {'Content-Type': 'application/json'},
                "statusCode"     : status_code,
                "body"           : Misc.json_format({'text': text})
            }
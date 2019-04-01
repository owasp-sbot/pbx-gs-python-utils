import json

from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc


def run(event, context):
    team_id = 'T7F3AUXGV'
    channel = 'DDKUZTK6X'
    text = "in API Gateway test..."
    attachments = [ {'text': "{0}".format(Misc.json_format(event)) , 'color':'good'}]
    #attachments = [{'text': "{0}".format(event), 'color': 'good'}]

    slack_message(text, attachments, channel,team_id)

    result = Misc.json_format({'text': text})
    return {
                'headers'        : {'Content-Type': 'application/json'},
                "statusCode"     : 209,
                "body"           : result
            }
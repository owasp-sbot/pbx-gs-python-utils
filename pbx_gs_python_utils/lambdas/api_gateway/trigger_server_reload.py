import json

from utils.Lambdas_Helpers import slack_message
from utils.Misc import Misc
from utils.aws.Lambdas import Lambdas


def run(event, context):
    team_id = 'T7F3AUXGV'
    channel = 'DDKUZTK6X'
    text = ":robot_face: In trigger_server_reload lambda function \n"

    payload = {"params": ["server", "reload"], "channel": channel, 'team_id': team_id}
    result  = Lambdas('gs.elastic_jira').invoke(payload)

    attachments = [{'text': result, 'color': 'good'}]

    slack_message(text, attachments, channel,team_id)

    result = Misc.json_format({'text': text})
    return {
                'headers'        : {'Content-Type': 'application/json'},
                "statusCode"     : 209,
                "body"           : result
            }
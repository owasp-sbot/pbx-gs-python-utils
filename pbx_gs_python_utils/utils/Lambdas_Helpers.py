import sys
sys.path.append('.')
from utils.aws.Lambdas import Lambdas


def log_to_elk(message, data = None, index = "gs_bot_logs", level = "debug", category = "API_GS_Bot"):
    payload = {
                "index"    : index    ,
                "level"    : level    ,
                "message"  : message  ,
                "category" : category ,
                "data"     : data
              }

    Lambdas('utils_log_to_elk').invoke_async(payload)

def slack_message(text, attachments = [], channel = 'GBMGMK88Z', team_id='T7F3AUXGV'):  # GBMGMK88Z is the 'from-aws-lambda' channel in the GS-CST Slack workspace
    payload = {
                'text'        : text        ,
                'attachments' : attachments ,
                'channel'     : channel     ,
                'team_id'     : team_id
              }
    Lambdas('utils_slack_message').invoke_async(payload)
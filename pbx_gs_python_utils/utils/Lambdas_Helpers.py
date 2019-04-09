import sys

from osbot_aws.apis.Lambda import Lambda

sys.path.append('.')

def log_info(message, data = None, index = "gs_bot_logs",category = "API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='info', category=category)

def log_debug(message, data=None, index="gs_bot_logs", category="API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='debug', category=category)

def log_error(message, data = None, index = "gs_bot_logs", category = "API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='error', category=category)

def log_to_elk(message, data = None, index = "gs_bot_logs", level = "debug", category = "API_GS_Bot"):
    payload = {
                "index"    : index    ,
                "level"    : level    ,
                "message"  : message  ,
                "category" : category ,
                "data"     : data
              }

    response = Lambda('pbx_gs_python_utils.lambdas.utils.log_to_elk').invoke_async(payload)
    return "{0}".format(response)

def slack_message(text, attachments = [], channel = 'GDL2EC3EE', team_id='T7F3AUXGV'):  # GBMGMK88Z is the 'from-aws-lambda' channel in the GS-CST Slack workspace
    payload = {
                'text'        : text        ,
                'attachments' : attachments ,
                'channel'     : channel     ,
                'team_id'     : team_id
              }
    Lambda('pbx_gs_python_utils.lambdas.utils.slack_message').invoke_async(payload)
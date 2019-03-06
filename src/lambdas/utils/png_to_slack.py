import base64
import tempfile

from utils.Files import Files
from   utils.Lambdas_Helpers import slack_message
from utils.aws.s3 import S3
from   utils.aws.secrets     import Secrets
from   utils.aws.Lambdas     import    load_dependency


def send_file_to_slack(file_path, title, bot_token, channel):                  # refactor into Slack_API class
    load_dependency('requests')          ;   import requests

    my_file = {
        'file': ('/tmp/file.png', open(file_path, 'rb'), 'png')
    }

    payload = {
        "filename"  : '{0}.png'.format(title),
        "token"     : bot_token,
        "channels"  : [channel],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'send png file: {0}'.format(title)


def run(event, context):

    channel         = event.get('channel')
    png_data        = event.get('png_data')
    s3_bucket       = event.get('s3_bucket')
    s3_key          = event.get('s3_key')
    title           = event.get('title')
    team_id         = event.get('team_id')
    aws_secrets_id  = event.get('aws_secrets_id')
    if  team_id == 'T7F3AUXGV': aws_secrets_id = 'slack-gs-bot'             # hard coded values
    if  team_id == 'T0SDK1RA8': aws_secrets_id = 'slack-gsbot-for-pbx'      # need to move to special function

    bot_token       = Secrets(aws_secrets_id).value()

    if png_data:
        #(fd, tmp_file) = tempfile.mkstemp('png')
        tmp_file = Files.temp_file('.png')
        with open(tmp_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
    else:
        if s3_bucket and s3_key:
            tmp_file = S3().file_download_and_delete(s3_bucket, s3_key)
        else:
            return None

    return send_file_to_slack(tmp_file, title, bot_token, channel)

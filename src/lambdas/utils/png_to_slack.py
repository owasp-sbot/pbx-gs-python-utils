import base64
import tempfile

from utils.Files import Files
from   utils.Lambdas_Helpers import slack_message
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
    title           = event.get('title')
    team_id         = event.get('team_id')
    aws_secrets_id  = event.get('aws_secrets_id')
    if  team_id == 'T7F3AUXGV':
        aws_secrets_id = 'slack-gs-bot'

    bot_token       = Secrets(aws_secrets_id).value()

    (fd, tmp_file) = tempfile.mkstemp('png)')

    with open(tmp_file, "wb") as fh:
        fh.write(base64.decodebytes(png_data.encode()))

    return send_file_to_slack(tmp_file, title, bot_token, channel)

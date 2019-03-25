import base64
import tempfile

from utils.Files import Files
from   utils.Lambdas_Helpers import slack_message
from   utils.aws.secrets     import Secrets
from   utils.aws.Lambdas     import    load_dependency


def send_file_to_slack(file_path, title, bot_token, channel):                  # refactor into Slack_API class
    load_dependency('requests')          ;   import requests

    my_file = {
        'file': ('/tmp/file.pdf', open(file_path, 'rb'), 'pdf')
    }

    payload = {
        "filename"  : '{0}.pdf'.format(title),
        "token"     : bot_token,
        "channels"  : [channel],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'send pdf: {0}'.format(title)


def run(event, context):

    channel         = event.get('channel')
    pdf_data        = event.get('pdf_data')
    title           = event.get('title')
    aws_secrets_id  = event.get('aws_secrets_id')
    bot_token       = Secrets(aws_secrets_id).value()

    (fd, tmp_file) = tempfile.mkstemp('pdf)')

    with open(tmp_file, "wb") as fh:
        fh.write(base64.decodebytes(pdf_data.encode()))

    return send_file_to_slack(tmp_file, title, bot_token, channel)

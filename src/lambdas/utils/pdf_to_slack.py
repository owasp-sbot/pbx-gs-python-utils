import base64
import tempfile

from utils.Files import Files
from   utils.Lambdas_Helpers import slack_message
from   utils.aws.secrets     import Secrets
from   utils.aws.Lambdas     import    load_dependency


def upload_png_file(channel_id, file):
    import requests
    bot_token = Secrets('slack-gs-bot').value()
    my_file = {
        'file': ('/tmp/file.pdf', open(file, 'rb'), 'pdf')
    }

    payload = {
        "filename"  : 'file.pdf',
        "token"     : bot_token,
        "channels"  : [channel_id],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'image sent .... '


def run(event, context):
    load_dependency('requests')

    channel         = event.get('channel')
    pdf_data        = event.get('pdf_data')
    (fd, tmp_file) = tempfile.mkstemp('png)')
    slack_message(len(pdf_data), [], channel)

    with open(tmp_file, "wb") as fh:
        fh.write(base64.decodebytes(pdf_data.encode()))

    return upload_png_file(channel, tmp_file)
    return Files.find('/tmp/*')
    return {}

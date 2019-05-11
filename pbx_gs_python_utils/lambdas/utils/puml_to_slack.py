import base64
import tempfile
import requests
from   osbot_aws.apis        import Secrets
from   osbot_aws.apis.Lambdas        import Lambdas


def upload_png_file(channel_id, file):
    bot_token = Secrets('slack-gs-bot').value()
    my_file = {
        'file': ('/tmp/myfile.png', open(file, 'rb'), 'png')
    }

    payload = {
        "filename"  : 'image.png',
        "token"     : bot_token,
        "channels"  : [channel_id],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'image sent .... '


def run(event, context):
    channel         = event['channel']
    puml            = event['puml']
    puml            = puml.replace('&lt;', '<').replace('&gt;', '>')
    (fd, tmp_file)  = tempfile.mkstemp('png)')
    puml_to_png     = Lambda('utils.puml_to_png').invoke
    result          = puml_to_png({"puml": puml })


    with open(tmp_file, "wb") as fh:
        fh.write(base64.decodebytes(result['png_base64'].encode()))

    return upload_png_file(channel, tmp_file)

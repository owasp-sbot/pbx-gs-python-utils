import base64
import tempfile
import requests

from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk
from   utils.aws.secrets        import Secrets
from   utils.aws.Lambdas        import Lambdas


def upload_png_file(team_id, channel_id, file):
    log_to_elk("[upload_png_file]: {0} {1} {2}".format(team_id,channel_id,file))
    bot_token = resolve_bot_token(team_id)
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


def resolve_bot_token(team_id):                                                # to refactor
    if team_id == '...':    return Secrets('slack-gs-bot'       ).value()
    if team_id == '...':    return Secrets('slack-gsbot-for-pbx').value()

    return Secrets('slack-gs-bot').value()


def run(event, context):
    channel         = event['channel']
    team_id         = event.get('team_id')
    puml            = event['puml']
    puml            = puml.replace('&lt;', '<').replace('&gt;', '>')
    (fd, tmp_file)  = tempfile.mkstemp('.png')
    puml_to_png     = Lambda('utils.puml_to_png').invoke
    result          = puml_to_png({"puml": puml })


    with open(tmp_file, "wb") as fh:
        fh.write(base64.decodebytes(result['png_base64'].encode()))

    return upload_png_file(team_id,channel, tmp_file)

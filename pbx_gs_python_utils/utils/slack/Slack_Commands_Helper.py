import pprint
from time import time

from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message, log_to_elk


class Slack_Commands_Helper:

    def __init__(self, target):
        self.target        = target
        self._show_duration = False

    def available_methods(self):
        return  [func for func in dir(self.target) if
                    callable(getattr(self.target, func)) and not func.startswith("_")]

    def help(self, prefix = ""):
        help_text = ""
        for command in self.available_methods():
            help_text += " • {0}\n".format(command)
        attachments = API_Slack_Attachment(help_text, 'good')
        text = prefix + "*Here are the `{0}` commands available:*".format(self.target.__name__)
        return text, attachments.render()

    def invoke(self, team_id=None, channel=None, params=None):
        if params is None: params = []
        attachments = []
        if len(params) == 0:
            (text, attachments) = self.help()
        else:
            original_params = list(params)
            command = params.pop(0)                                                 # extract first element from the array
            if command in self.available_methods():
                method  = getattr(self.target, command)
                try:
                    start = time()
                    result = method(team_id, channel, params)
                    if type(result).__name__ == 'tuple':
                        text, attachments = result
                    else:
                        text, attachments = result,[]
                    if text is None and self._show_duration:
                        duration = time() - start
                        text= 'completed execution in `{0:.0f}` secs'.format(duration)
                except Exception as error:
                    text = ':red_circle: Error processing params `{0}`: _{1}_'.format(original_params, pprint.pformat(error))
                    log_to_elk("Error in Lambda_Graph.handle_lambda_event :{0}".format(text), level='error')
            else:
                (text,attachments) = self.help(':red_circle: command not found `{0}`\n\n'.format(command))
        if channel and text is not None:                                           # if there is a text value, then send it as a slack message
            slack_message(text, attachments, channel, team_id)
        return text,attachments

    def show_duration(self,value):
        self._show_duration = value
        return self
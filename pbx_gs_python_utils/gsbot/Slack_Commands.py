import json

from pbx_gs_python_utils.utils.Misc import Misc


def slack(team_id):
    from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
    return API_Slack(team_id=team_id)

class Slack_Commands:

    @staticmethod
    def username_to_id(team_id=None, channel=None, params=[]):
        if len(params) >0:
            username_id = params.pop().replace('<@', '').replace('>', '')
            text = "The id for the provided user is: {0}".format(username_id)
            return text, []

    @staticmethod
    def stats(team_id=None, channel=None, params=None):
        stats = {
            "# of users" : len(list(set(slack(team_id).users())))
        }
        return Misc.json_format(stats)

    @staticmethod
    def user_info(team_id=None, channel=None, params=None):
        if len(params) > 0:
            user_name = ' '.join(params)
            users = slack(team_id).users()
            user = users.get(user_name)
            if user:
                return "```{0}```".format(Misc.json_format(user))
            for user in users.values():
                if user.get('id') == user_name or user.get('real_name') == user_name:
                    return "```{0}```".format(Misc.json_format(user))
            return ":exclamation: Sorry, could not find user with alias `{0}`".format(user_name)



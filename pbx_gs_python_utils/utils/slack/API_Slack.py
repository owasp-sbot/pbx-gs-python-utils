from utils.Dev import Dev
from utils.aws.secrets import Secrets
from slackclient       import SlackClient
from utils.aws.Lambdas import Lambdas


class API_Slack:
    def __init__(self,  channel = 'GDL2EC3EE', team_id=None):
        bot_token      = self.resolve_bot_token(team_id)
        self.channel   = channel
        self.slack     = SlackClient(bot_token)

    # need to find a better solution to handle this
    def resolve_bot_token(self, team_id):  # to refactor
        if team_id == 'T7F3AUXGV':    return Secrets('slack-gs-bot').value()
        if team_id == 'T0SDK1RA8':    return Secrets('slack-gsbot-for-pbx').value()

        return Secrets('slack-gs-bot').value()          # default to GS CST Slack org

    def add_reaction(self, ts, reaction):
        return self.slack.api_call( "reactions.add", channel =self.channel, name = reaction , timestamp=ts )

    def team_logins(self, count = 100, pages = 1):
        logins = []
        for page in range(1,pages + 1):
            data  = self.slack.api_call('team.accessLogs', count = count, page = page)
            entries = data.get('logins')
            #print('[API Slack][team_logins] got {0} entries for page {1}'.format(len(entries), page))
            logins.extend(entries)
        return logins

    def channels_history(self,channel):
        return self.slack.api_call("channels.history", channel = channel)

    def channels_public(self):
        channels = {}
        cursor = None
        while cursor != '':
            data = self.slack.api_call("channels.list", cursor = cursor)
            cursor = data.get('response_metadata').get('next_cursor')
            for channel in data['channels']:
                channels[channel['name']] = channel
        return channels

    def channels_private(self):
        channels = {}
        for channel in self.slack.api_call("conversations.list", types='private_channel')['channels']:
            channels[channel['name']] = channel
        return channels

    def delete_message(self,ts, channel):
        return self.slack.api_call("chat.delete", channel=channel,ts=ts)

    def get_channel(self, channel):
        return self.slack.api_call("channels.info", channel=channel)

    def get_messages(self,channel,limit=10):
        messages = self.slack.api_call("conversations.history", channel=channel, limit=limit).get('messages')
        Dev.pprint(messages)
        return [message.get('text') for message in messages]

    def send_message(self, text, attachments = [], channel = None):
        if channel is None:
            channel = self.channel
        return self.slack.api_call("chat.postMessage",
                            channel     = channel,
                            text        = text ,
                            attachments = attachments)

    def set_channel(self, channel):
        self.channel = channel
        return self

    # def postMessage(self,used_id):
    #     return self.slack.api_call("chat.postMessage",
    #                                channel=self.channel,
    #
    #                       used_  =used_id)
    def user(self,user_id):
        return self.slack.api_call("users.info", user=user_id)

    def users(self):
        users = {}
        cursor = None
        while cursor != '':
            data = self.slack.api_call("users.list", cursor = cursor )
            cursor = data.get('response_metadata').get('next_cursor')
            for user in data.get('members'):
                users[user['name']] = user
        return users


    ## methods using lambdas

    def dot_to_slack(self, dot):
        payload = {"dot"    : dot          ,
                   "channel": self.channel }
        return Lambdas('utils.dot_to_slack').invoke(payload)

    def puml_to_slack(self, puml):
        payload = {"puml"   : puml          ,
                   "channel": self.channel  }
        return Lambdas('utils.puml_to_slack').invoke(payload)




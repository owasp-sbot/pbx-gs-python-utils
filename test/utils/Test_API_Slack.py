import unittest

from utils.Misc import Misc
from utils.aws.secrets import Secrets
from utils.slack.API_Slack import API_Slack
from utils.Dev import Dev

class Test_API_Slack(unittest.TestCase):

    def setUp(self):
        self.channel = 'GDL2EC3EE' #''gs-bot-tests'
        self.api     = API_Slack(self.channel)

    def test_add_reaction(self):
        response = self.api.send_message("Testing reaction")
        ts       = response['message']['ts']
        response = self.api.add_reaction(ts, "thumbsup")
        assert response['ok'] is True

    def test_channels_public(self):
        channels = self.api.channels_public()
        assert len(set(channels)) > 40
        assert channels['random']['id'] == 'C7EUMACGJ'

    def test_channels_private(self):
        channels = self.api.channels_private()
        assert set(channels) == {'from-aws-lambda', 'gs-bot-tests', 'gs-cst-aws-coding', 'lan-turtle'}
        assert channels['gs-bot-tests']['id'] == 'GDL2EC3EE'

    def test_delete_message(self):
        reply_send   = self.api.send_message('to delete 123')      # send message
        ts           = reply_send['message']['ts']                 # get timestamp of message posted
        reply_delete = self.api.delete_message(ts, self.channel)   # delete message
        assert reply_delete['ok'] is True
        assert reply_delete['ts'] == ts

    def test_get_channel(self):
        response = self.api.get_channel('DDKUZTK6X')
        Dev.pprint(response)

    def test_get_messages(self):
        assert len(self.api.get_messages('DDKUZTK6X')) == 10

    def test_send_message(self):
        text    = 'testing api_slack 123'
        result = self.api.send_message(text)
        del result['message']['ts']
        assert result['ok'] is True

        Dev.pprint(result['message'])
        assert result['message'] == {   'attachments': []                 ,
                                        'bot_id'     : 'BDKLUMX4K'        ,
                                        'subtype'    : 'bot_message'      ,
                                        'text'       : text               ,
                                        'type'       : 'message'          ,
                                        'username'   : 'gs-bot'           }

    def test_user(self):
        user_id = 'UDK5W7W3T'
        result = self.api.send_message(user_id)
        assert result['message']['username'] == 'gs-bot'

    def test_users(self):
        users = self.api.users()
        assert len(set(users)) > 120
        assert users['dinis.cruz']['id'] == 'U7ESE1XS7'
        assert users['gsbot'     ]['id'] == 'UDK5W7W3T'

        #Dev.pprint(users)


    def test_send_and_receive_messages(self):
        result = self.api.send_message('<@UDK5W7W3T> hello', channel='DDKUZTK6X')
        Misc.wait(1)
        messages = self.api.get_messages(channel='DDKUZTK6X',limit=2)
        Dev.pprint(messages)


    ## Buttons and interaction

    def test____message_with_button(self):
        message = {
                "text": "Would you like to play a game?",
                "attachments": [
                    {
                        "aaaaa" : "bbbbb",
                        "ccccc" : "ddddd",
                        "text": "Choose a game to play",
                        "fallback": "You are unable to choose a game",
                        "callback_id": "wopr_game",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "game",
                                "text": "Chess",
                                "type": "button",
                                "value": "chess"
                            },
                            {
                                "name": "game",
                                "text": "Falken's Maze",
                                "type": "button",
                                "value": "maze"
                            },
                            {
                                "name": "THE NAME ",
                                "text": "BETTER OPTION",
                                "type": "button",
                                "value": "THE VALUE"
                            },
                            {
                                "name": "game",
                                "text": "Thermonuclear War",
                                "style": "danger",
                                "type": "button",
                                "value": "war",
                                "confirm": {
                                    "title": "Are you sure?",
                                    "text": "Wouldn't you prefer a good game of chess?",
                                    "ok_text": "Yes",
                                    "dismiss_text": "No"
                                }
                            },
                            {
                                    "name": "games_list",
                                    "text": "Pick a game...",
                                    "type": "select",
                                    "options": [
                                        {
                                            "text": "Hearts",
                                            "value": "hearts"
                                        },
                                        {
                                            "text": "Bridge",
                                            "value": "bridge"
                                        },
                                        {
                                            "text": "Checkers",
                                            "value": "checkers"
                                        },
                                        {
                                            "text": "Chess",
                                            "value": "chess"
                                        },
                                        {
                                            "text": "Poker",
                                            "value": "poker"
                                        },
                                        {
                                            "text": "Falken's Maze",
                                            "value": "maze"
                                        },
                                        {
                                            "text": "test 1",
                                            "value": "test 1"
                                        }
                                        ,
                                        {
                                            "text": "test 2",
                                            "value": "test 2"
                                        }
                                        ,
                                        {
                                            "text": "test 3",
                                            "value": "test 3"
                                        }
                                        ,
                                        {
                                            "text": "test 4",
                                            "value": "test 4"
                                        }
                                        ,
                                        {
                                            "text": "test 4",
                                            "value": "test 4"
                                        }
                                        ,
                                        {
                                            "text": "test 5",
                                            "value": "test 5"
                                        }
                                    ]
                                }

                        ]
                    }
                ]
            }
        self.api.send_message(message['text'], message['attachments'])

    ## methods using lambdas

    def test_dot_to_slack(self):
        dot = 'digraph {\n a->b \n}'
        assert self.api.dot_to_slack(dot) == 'image sent .... '

    def test_puml_to_slack(self):
        puml = "@startuml \n aaa->bbb \n @enduml"
        assert self.api.puml_to_slack(puml) == 'image sent .... '



    ## test using the API

    def test___send_message_to_gsbot(self):
        #self.api.channel = 'UDK5W7W3T'  # gs bot
        response = self.api.send_message("<@/jira>")
        Dev.pprint(response)



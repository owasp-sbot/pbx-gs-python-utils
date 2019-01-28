import base64
import os
import tempfile

import  pydot
import  unittest
from    utils.Dev              import Dev
from    utils.Show_Img import Show_Img
from    utils.aws.Lambdas      import Lambdas


class Test_Lambda_slack_message(unittest.TestCase):
    def setUp(self):
        self.slack_message = Lambdas('utils.slack_message', path_libs = '../_lambda_dependencies/slack')

    def test_update_invoke(self):
        channel     = "gs-bot-tests"
        text        = ":point_right: an message from lambda"
        attachments = [ {"text" : "an attachment (good)" , "color": "good"}, {"text" : "an attachment (danger)" , "color": "danger"}]
        result      = self.slack_message.upload_and_invoke({"channel" : channel ,"text" :text, "attachments": attachments })
        del result['message']['ts']
        assert result['ok'] is True
        assert result['message'] == { 'attachments' : [ {   'color'     : '2eb886'                   ,
                                                            'fallback'  : 'an attachment (good)'     ,
                                                            'id'        : 1                          ,
                                                            'text'      : 'an attachment (good)'    },
                                                        {   'color'     : 'a30200'                   ,
                                                            'fallback'  : 'an attachment (danger)'   ,
                                                            'id'        : 2                          ,
                                                            'text'      : 'an attachment (danger)' }],
                                     'bot_id'       : 'BDKLUMX4K'                                    ,
                                     'subtype'      : 'bot_message'                                  ,
                                     'text'         : ':point_right: an message from lambda'         ,
                                     'type'         : 'message'                                      ,
                                     'username'     : 'gs-bot'                                       }

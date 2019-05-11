import  unittest

from osbot_aws.apis.Lambda import Lambda

class test_slack_message(unittest.TestCase):
    def setUp(self):
        self.slack_message = Lambda('pbx_gs_python_utils.lambdas.utils.slack_message')

    def test_invoke(self):
        channel     = "gs-bot-tests"
        text        = ":point_right: an message from lambda"
        attachments = [ {"text" : "an attachment (good)" , "color": "good"}, {"text" : "an attachment (danger)" , "color": "danger"}]
        result      = self.slack_message.invoke({"channel" : channel ,"text" :text, "attachments": attachments })
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

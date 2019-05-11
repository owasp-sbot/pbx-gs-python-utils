from unittest import TestCase

from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.Lambdas_Helpers            import slack_message
from osbot_aws.apis.Lambda import Lambda

class test_API_Slack_Attachment(TestCase):

    def setUp(self):
        self.api = API_Slack_Attachment()

    # def test__update_lambda(self):
    #     Lambda('gs.jira_dialog').update()

    # def test____update_Lambda_Slack_Integration(self):
    #     path_libs = '../_lambda_dependencies/elastic-slack'
    #     self.jira_issues = Lambda('gs.slack_interaction').update()

    def test_select(self):
        text          =  "...testing select attachment"
        (self.api.set_text('this is the attachment text')
             .set_callback_id ("button-test")
             .set_color       ("#0055AA")
             .add_button      ("name 1", "text 1", "type 3", "primary")
             .add_button      ("name 2", "text 2", "type 3", "danger")
             .add_select      ("name", "pick a value",[("text 1", "value-1"), ("text 2", "value-2")])
             .add_select_users("user", "pick a user")  )

        attachments = self.api.render()
        slack_message(text, attachments, 'DDKUZTK6X')

    def test_add_select_user_data_source(self):
        (self.api.set_text('here are the multiple data sources'     )
             .set_callback_id         ("issue-suggestion"           )
             .add_select_users        ("user", "pick a user"        )
             .add_select_channels     ("user", "pick a channel"     )
             .add_select_conversations("user", "pick a conversation")
             .add_select_external     ("key", "pick an Key"        ))   
        slack_message("", self.api.render(), 'DDKUZTK6X')

    def test_render(self):
        self.api.set_text       ('this is the attachment text'            ) \
                .set_callback_id("button-test")                      \
                .add_button     ("name 1", "text 1", "type 3", "primary") \
                .add_button     ("name 2", "text 2", "type 3", "danger" )
        attachments = self.api.render()
        text = None  # 'main text'
        slack_message(text, attachments, 'DDKUZTK6X')
from unittest                   import TestCase

from pbx_gs_python_utils.utils.slack.API_Slack_Attachment   import API_Slack_Attachment
from pbx_gs_python_utils.utils.slack.API_Slack_Dialog       import API_Slack_Dialog
from pbx_gs_python_utils.utils.Lambdas_Helpers              import slack_message


class test_API_Slack_Dialog(TestCase):

    def setUp(self):
        self.api_attach = API_Slack_Attachment()
        self.api_dialog = API_Slack_Dialog()


    # def test__update_lambda(self):
    #     Lambda('gs.jira_dialog').update_with_src()
    #
    # def test____update_Lambda_Slack_Integration(self):
    #     self.jira_issues = Lambda('gs.slack_interaction').update_with_src()

    def test_test_render(self):
        dialog = self.api_dialog.test_render()
        dialog.get('title') == 'This is a test'

    def test__create_button_to_test_dialog(self):
        #Lambda('gs.jira_dialog').update_with_src()

        self.api_attach.set_text       ('Click on button below to test dialog'    ) \
                       .set_callback_id("button-dialog-test"                      ) \
                       .add_button     ("button", "open dialog", "open", "primary")
        attachments = self.api_attach.render()
        slack_message("", attachments, 'DDKUZTK6X')



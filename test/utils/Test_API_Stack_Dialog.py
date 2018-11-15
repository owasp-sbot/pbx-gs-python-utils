from unittest                   import TestCase

from utils.API_Slack_Attachment import API_Slack_Attachment
from utils.API_Slack_Dialog     import API_Slack_Dialog
from utils.Dev import Dev
from utils.Lambdas_Helpers      import slack_message
from utils.aws.Lambdas import Lambdas


class Test_API_Slack_Dialog(TestCase):

    def setUp(self):
        self.api_attach = API_Slack_Attachment()
        self.api_dialog = API_Slack_Dialog()


    def test__update_lambda(self):
        Lambdas('gs.jira_dialog').update()

    def test____update_Lambda_Slack_Integration(self):
        from utils.aws.Lambdas import Lambdas
        path_libs = '../_lambda_dependencies/elastic-slack'
        self.jira_issues = Lambdas('gs.slack_interaction', path_libs=path_libs).update()

    def test_test_render(self):
        dialog = self.api_dialog.test_render()
        #Dev.pprint(dialog)

    def test__create_button_to_test_dialog(self):
        Lambdas('gs.jira_dialog').update()

        self.api_attach.set_text       ('Click on button below to test dialog'    ) \
                       .set_callback_id("button-dialog-test"                      ) \
                       .add_button     ("button", "open dialog", "open", "primary")
        attachments = self.api_attach.render()
        slack_message("", attachments, 'DDKUZTK6X')



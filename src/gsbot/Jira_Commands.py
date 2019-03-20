# These are the methods to be called inside the Sync Server
from api_jira.API_Jira import API_Jira
from utils.Dev import Dev


class Jira_Commands:

    gsbot_projects = ['GSBOT','IA','SEC','RISK','VULN']

    @staticmethod
    def _check_params(params, expected_params):
        if len(params) != len(expected_params):
            text = ':red_circle: For this command, you need to provide the following parameters: '
            attachment_text = ''
            for expected_param in expected_params:
                attachment_text += '- {0} \n'.format(expected_param)
            attachments = [{'text': attachment_text}]
            return text, attachments
        return None, None

    @staticmethod
    def projects(team_id=None, channel=None, params=None):
        if channel and team_id:
            return ":point_right: Here are the projects that GSBot currently supports: `{0}`".format(Jira_Commands.gsbot_projects)
        return Jira_Commands.gsbot_projects

    @staticmethod
    def issue(team_id=None, channel=None, params=None):
        (text, attachments) = Jira_Commands._check_params(params, ['Issue Id'])
        if text: return text, attachments

        issue_id,  = params
        Dev.pprint(issue_id)
        project = issue_id.split('-').pop(0)
        projects = Jira_Commands.gsbot_projects
        if project not in projects:
            return ":rec_circle: project `{0}` is currently not available. The projects currently supported are: `{1}`".format(project,projects)

        return API_Jira().issue(issue_id)

    @staticmethod
    def version(team_id=None, channel=None, params=None):
        return "0.11.1"

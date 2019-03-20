# These are the methods to be called inside the Sync Server
from api_jira.API_Jira import API_Jira


class Jira_Commands:

    @staticmethod
    def projects(team_id=None, channel=None, params=None):
        jira = API_Jira()
        projects = jira.projects()
        return "there are {0} projects in jira ...".format(len(projects))

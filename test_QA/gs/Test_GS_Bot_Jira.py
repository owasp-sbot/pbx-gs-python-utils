import unittest

from pbx_gs_python_utils.gs.GS_Bot_Jira         import GS_Bot_Jira
from pbx_gs_python_utils.utils.Dev              import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers  import slack_message
from pbx_gs_python_utils.utils.aws.Lambdas      import Lambdas


class Test_GS_Bot_Jira(unittest.TestCase):
    def setUp(self):
        self.api     = GS_Bot_Jira()
        self.channel = 'DDKUZTK6X'                  # gsbot

    def test_handle_request(self):
        event = {}
        result = self.api.handle_request(event)

        Dev.pprint(result)

    def test_handle_request___no_command(self):
        result = self.api.handle_request({})
        assert result == { 'attachments': [],
                           'text': ':point_right: no command received, see `jira help` for a list of available commands`'}

    def test_handle_request___issue_no_id(self):
        result = self.api.handle_request( { "params" : ["issue"] } )
        assert result == {'attachments': [], 'text': ':exclamation: you must provide an issue id '}

    def test_handle_request___issue_bad_id(self):
        result = self.api.handle_request( { "params" : ["issue", "AAAA"] } )
        assert result == { 'attachments': [],
                           'text': '....._Fetching data for '
                           '*<https://jira.photobox.com/browse/AAAA|AAAA>* _from ES index:_ '
                           '*jira*'}

    def test_handle_request___org_chart(self):
        result = self.api.handle_request( { "params" : ["graph", "org-chart"] } )
        print(result)
        #assert result == {'attachments': [], 'text': ':fireworks: ...generating org chart from ELK data...'}


    def test_resolve_es_index(self):
        assert self.api.resolve_es_index('AAAA'    ) == 'jira'
        assert self.api.resolve_es_index('SEC-1'   ) == 'sec_project'
        assert self.api.resolve_es_index('SEC-'    ) == 'sec_project'
        assert self.api.resolve_es_index('SEC-1000') == 'sec_project'


    def test_cmd_created_in_last(self):
        params = ["20h"]
        result = self.api.cmd_created_in_last(params)
        Dev.pprint(result)

    def test_cmd_created_between(self):
        params = ["now-24h","now"]
        result = self.api.cmd_created_between(params)
        Dev.pprint(result)


    def test_cmd_links(self):
        #result = self.api.cmd_links(['links', 'risk-1496','down','1']    , self.channel, None)
        #result = self.api.cmd_links(['links', 'graph_1G0', 'down', '2'  ], self.channel, None)
        #result = self.api.cmd_links(['links', 'IA-386', 'children', '2' ], self.channel, None)
        #result = self.api.cmd_links(['links', 'IA-386', 'children', '5', 'it_assets'], self.channel, None)
        #result = self.api.cmd_links(['links', 'IA-386', 'children', '5', 'by_labels'], self.channel, None)

        #result = self.api.cmd_links(['links', 'graph_1G3', 'all', '2'], self.channel, None)
        result = self.api.cmd_links(['links', 'SEC-10965', 'all', '1'])
        Dev.pprint(result)

    def test_cmd_links__no_channel(self):
        result = self.api.cmd_links(['links', 'IA-403', 'down', '0'], None, None)
        Dev.pprint(result)

    def test_cmd_links__only_create(self):
        result = self.api.cmd_links(params=['links', 'IA-403', 'down', '0'], only_create=True)
        Dev.pprint(result)

    def test_cmd_help(self):
        result = self.api.cmd_help()
        Dev.pprint(result)

    def test_cmd_server(self):
        result = self.api.cmd_server(['server','status'])
        Dev.pprint(result)

    def test_cmd_up(self):
        result = self.api.cmd_up(['links', 'IA-404', '2'], team_id='T7F3AUXGV', channel='DDKUZTK6X')
        Dev.pprint(result)

    def test_cmd_down(self):
        result = self.api.cmd_down(['links', 'IA-404', '2'], team_id='T7F3AUXGV', channel='DDKUZTK6X')
        Dev.pprint(result)

    def test_cmd_sync_sheet(self):
        file_id = '1MHU2Av4tI0FaktjWjbIpFH_zwb-804CAn-MQLuqaq1A'
        result = self.api.cmd_sync_sheet(['', file_id], team_id='T7F3AUXGV', channel='DDKUZTK6X')
        Dev.pprint(result)

    # test via lambda


    def test__cmd_links__via_lambda(self):
        elastic_jira = Lambdas('gs.elastic_jira')
        payload = {"params": ["links","FACT-47", "up", "3"], "channel": "DDKUZTK6X"}

        result = elastic_jira.update_with_src().invoke(payload)

        text        = result['text']
        attachments = result['attachments']
        channel     = 'DDKUZTK6X'
        slack_message(text, attachments,channel)

        Dev.print(text)

    def test__cmd_server__via_lambda(self):
        elastic_jira = Lambdas('gs.elastic_jira')
        payload = {"params": ["server", "status"], "channel": "DDKUZTK6X", 'team_id': 'T7F3AUXGV'}

        result = elastic_jira.update_with_src().invoke(payload)
        Dev.pprint(result)

    # Regression tests

    def test__cmd_links__unhandled_int_int(self):
        result = self.api.cmd_links(['links', 'SEC-10965', '1','all'])  #was : ValueError("invalid literal for int() with base 10: 'all'",)
        Dev.pprint(result)

    # update lambda

    def test__lambda_update(self):
        Lambdas('gs.elastic_jira').update_with_src()




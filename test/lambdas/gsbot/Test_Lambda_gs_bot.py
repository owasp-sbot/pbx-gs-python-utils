import unittest
from   utils.Dev        import *
from utils.aws.Lambdas import Lambdas


class Test_Lambda_gs_bot(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambdas('gsbot.lambda_gs_bot', memory = 3008)

    def test_lambda_update(self):
        self.step_lambda.update_with_src()


    def _send_command_message(self,command):
        payload = {'team_id': 'T7F3AUXGV',
                   'event': {'type': 'message',
                             'text': command,
                             'channel': 'DDKUZTK6X',
                             'user': 'U7ESE1XS7'}}
        return self.step_lambda.upload_and_invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_hello(self):
        response = self._send_command_message('hello')
        Dev.pprint(response)

    def test_version(self):
        response = self._send_command_message('version')
        Dev.pprint(response)

    def test_graph(self):
        response = self._send_command_message('graph')
        Dev.pprint(response)

    def test_graph(self):
        response = self._send_command_message('slack test')
        Dev.pprint(response)


    def test_run_log_files(self):
        #payload = { 'event': { 'text': '@gsbot From unit test' , 'channel':'GDL2EC3EE'}}
        #payload = {'event': {'text': '<@UDK5W7W3T> ec2_instances_details', 'channel': 'GDL2EC3EE'}}
        #text = "dot_render ```aaaa```"
        #Dev.pprint("digraph G {\n" + text + "\n }")
        #return
        #payload = {'event': {'text': 'dot_render ```another->test ```', 'channel': 'GDL2EC3EE'}}
        payload = {'event': {'text': 'plantuml ```aaa -> bbb```', 'channel': 'GDL2EC3EE'}}

        #payload = {'event': {'type':'message', 'text': 'jira issue SEC-9195', 'channel': 'GDL2EC3EE', "user": 'U7ESE1XS7'}}
        #payload = {'event': {'text': 'jira issue-links SEC-9195', 'channel': 'GDL2EC3EE', "user": 'U7ESE1XS7'}}

        #payload = { 'event': { 'type':'message', 'text': 'hello @gsbot' , 'channel':'GDL2EC3EE', 'user': 'U7ESE1XS7'} }

        #payload = {'event': { 'type':'link_shared', 'links': [{"url": "abc"}], 'channel': 'GDL2EC3EE', 'user': 'U7ESE1XS7'}}
        response = self.step_lambda.upload_and_invoke(payload) #== '200 OK'

        Dev.pprint(response)



    def test_test_posted_data(self):
        body = "payload=..."

        payload = {"body" : body}

        response = self.step_lambda.upload_and_invoke(payload)  # == '200 OK'
        Dev.pprint(response)


    def test_jira_test_buttons(self):
        payload = {'event': {'text': 'jira test', 'channel': 'GDL2EC3EE', "user": 'U7ESE1XS7', 'type':'message'}}
        response = self.step_lambda.upload_and_invoke(payload)  # == '200 OK'

        Dev.pprint(response)


    def test_time(self):
        payload = { 'event': { 'type':'message', 'text': '<@UDK5W7W3T> time' , 'channel':'GDL2EC3EE', 'user': 'U7ESE1XS7'} }
        assert self.step_lambda.upload_and_invoke(payload)  == '200 OK'
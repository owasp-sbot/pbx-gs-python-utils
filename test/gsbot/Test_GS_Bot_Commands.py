class Test_GS_Bot_Commands(unittest.TestCase):

    def test_hello(self):
        assert GS_Bot_Commands.hello({}              ) == ('Hello <@None>, how can I help you?',[])
        assert GS_Bot_Commands.hello({'user' : 'abc'}) == ('Hello <@abc>, how can I help you?',[])

    def test_time(self):
        Dev.pprint(GS_Bot_Commands.time({'user' : 'abc'}))

    def test_commands_available(self):
        result = GS_Bot_Commands.commands_available({})
        Dev.pprint(result)

    def test_bad_cmd(self):
        (text, attachment) = GS_Bot_Commands.bad_cmd({'text' : 'bbbb'})
        assert text == (':exclamation: Sorry, could not match provided command to a method: `bbbb`\n'
                        '*Here are the commands available*')

    def test_dot_render(self):
        slack_event = { "text" : "```A->B```", "channel" : "DDKUZTK6X"}
        result = GS_Bot_Commands.dot_render(slack_event, [])
        Dev.pprint(result)



    # def test_public_slack_channels(self):
    #     result = GS_Bot_Commands.public_slack_channels({})
    #     Dev.pprint(result)

    def test_ec2_instances_details(self):
        (text, attachment) = GS_Bot_Commands.ec2_instances_details({})

        Dev.pprint(text)
        Dev.pprint(attachment[0]['text'])

    def test_ec2_instances_status(self):
        (text, attachment) = GS_Bot_Commands.ec2_instances_status({})

        Dev.pprint(text)
        Dev.pprint(attachment)

    def test_method_logs_metadata_files(self):
        (text, attachment) = GS_Bot_Commands.ec2_instances_details({})

        Dev.print(text)
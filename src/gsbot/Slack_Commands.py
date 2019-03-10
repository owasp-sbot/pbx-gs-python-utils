class Slack_Commands:
    @staticmethod
    def test(team_id, channel, params):
        return "in slack: {0}".format(params)
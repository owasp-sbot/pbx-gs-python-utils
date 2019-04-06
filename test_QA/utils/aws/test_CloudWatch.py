from coverage.backunittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.aws.Cloud_Watch import Cloud_Watch


class test_Cloud_Watch(TestCase):

    def setUp(self):
        self.cloud_watch = Cloud_Watch()

    def test__init__(self):
        type(self.cloud_watch.cloudwatch).__name__ == 'CloudWatch'

    def test_log_group_create(self):
        name    = 'test_log_group'
        assert self.cloud_watch.log_group_exists(name) is False
        self.cloud_watch.log_group_create(name)
        assert self.cloud_watch.log_group_exists(name) is True
        assert self.cloud_watch.log_group_details(name).get('logGroupName') == name
        self.cloud_watch.log_group_delete(name)
        assert self.cloud_watch.log_group_exists(name) is False

    def test_log_groups(self):
        assert len(list(self.cloud_watch.log_groups())) > 1

    def test_logs(self):
        group_name  = 'awslogs-temp_task_on_temp_cluster_X29B3K'
        stream_name = 'awslogs-example/gs-docker-codebuild/f8ccf213-b642-466c-8458-86af9933eca9'
        messages    = self.cloud_watch.logs_get_messages(group_name, stream_name)
        Dev.pprint(messages)
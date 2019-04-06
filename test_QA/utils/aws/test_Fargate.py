import sys ; sys.path.append('..')

from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from pbx_gs_python_utils.utils.aws.Fargate import Fargate


class test_Fargate(TestCase):
    def setUp(self):
        self.fargate = Fargate()

    def test__init__(self):
        assert type(self.fargate.ecs).__name__ == 'ECS'

    # def test_cluster_delete(self):
    #     clusters_arns = self.fargate.clusters()
    #     result = self.fargate.cluster_delete(clusters_arns[0])
    #     Dev.pprint(result)

    def test_clusters(self):
        result = self.fargate.clusters()
        if len(result) > 0:
            assert 'arn:aws:ecs:' in result[0]

    def test_task_definitions(self):
        result = self.fargate.task_definitions()
        assert len(result) > 1
        assert ':task-definition/' in result[0]
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from pbx_gs_python_utils.utils.aws.Fargate import Fargate


class test_Fargate(TestCase):
    def setUp(self):
        self.fargate = Fargate()

    def test__init__(self):
        assert type(self.fargate.ecs).__name__ == 'ECS'

    def test_clusters(self):
        result = self.fargate.clusters()
        assert 'clusterArns' in set(result)
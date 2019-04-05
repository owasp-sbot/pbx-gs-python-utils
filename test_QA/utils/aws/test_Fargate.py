from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from pbx_gs_python_utils.utils.aws.Fargate import Fargate


class test_Fargate(TestCase):
    def setUp(self):
        self.fargate = Fargate()

    def test__init__(self):
        assert type(self.fargate.ecs).__name__ == 'ECS'

    def test_cluster_delete(self):
        clusters_arns = self.fargate.clusters()
        Dev.pprint(clusters_arns)
        #clusterArns' in set(result)

    def test_clusters(self):
        result = self.fargate.clusters()
        if len(result) > 0:
            assert 'arn:aws:ecs:' in result[0]
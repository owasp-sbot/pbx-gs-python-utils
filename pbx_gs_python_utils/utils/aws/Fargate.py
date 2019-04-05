import boto3


class Fargate:

    def __init__(self):
        self.ecs = boto3.client('ecs')

    def cluster_delete(self, cluster_arn):
        self.ecs.delete_cluster(cluster_arn)

    def clusters(self):
        return self.ecs.list_clusters().get('clusterArns')

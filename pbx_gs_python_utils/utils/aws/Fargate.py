import boto3


class Fargate:

    def __init__(self):
        self.ecs = boto3.client('ecs')

    def cluster_delete(self, cluster_arn):
        return self.ecs.delete_cluster(cluster=cluster_arn)

    def clusters(self):
        return self.ecs.list_clusters().get('clusterArns')

    def task_definitions(self):
        return self.ecs.list_task_definitions().get('taskDefinitionArns')

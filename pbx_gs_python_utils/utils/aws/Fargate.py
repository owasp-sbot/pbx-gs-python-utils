import boto3


class Fargate:

    def __init__(self):
        self.ecs = boto3.client('ecs')

    def clusters(self):
        return self.ecs.list_clusters()
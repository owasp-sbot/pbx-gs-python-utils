import boto3
import pprint

class Secrets:
    def __init__(self, id):
        self.aws_secrets = boto3.client('secretsmanager')
        self.id = id

    def create      (self, value):
        self.aws_secrets.create_secret( Name = self.id, SecretString = value)
        return self.exists()

    def deleted     (self):
        details = self.details()
        if details:
            return details.get('DeletedDate') is not None
        return False

    def delete      (self):
        self.aws_secrets.delete_secret(SecretId = self.id)
        return self.exists() is False

    def details     (self):
        try:
            return self.aws_secrets.describe_secret(SecretId = self.id)
        except:
            return None

    def exists      (self):
        return self.details() is not None and self.deleted() is False

    def print       (self):
        details = self.details()
        print(pprint.pformat(details))

    def undelete    (self):
        return self.aws_secrets.restore_secret(SecretId = self.id)

    def update      (self, value):
        self.aws_secrets.update_secret( SecretId = self.id, SecretString = value)
        return self.exists()

    def value               (self):
        if self.exists():
            return self.aws_secrets.get_secret_value(SecretId=self.id).get('SecretString')
        return None
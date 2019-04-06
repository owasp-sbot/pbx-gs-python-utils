import boto3

from pbx_gs_python_utils.utils.Dev import Dev


class Cloud_Watch:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.logs       = boto3.client('logs')

    def _invoke_via_paginator(self, api, method, field_id, **kwargs):
        paginator = api.get_paginator(method)
        for page in paginator.paginate(**kwargs):
            for id in page.get(field_id):
                yield id

    def log_group_create(self, name):
        self.logs.create_log_group(logGroupName=name)
        return self

    def log_group_delete(self, name):
        self.logs.delete_log_group(logGroupName=name)
        return self

    def log_group_exists(self, name):
        return self.log_group_details(name) is not None

    def log_group_details(self, name):
        for log_group in self.logs.describe_log_groups(logGroupNamePrefix= name).get('logGroups'):
            if log_group.get('logGroupName') == name:
                return log_group
        return None

    def log_groups(self):
        groups = {}
        for group in  self._invoke_via_paginator(self.logs, 'describe_log_groups', 'logGroups'): # self.logs.describe_log_groups().get('logGroups'):
            groups[group.get('logGroupName')] = group
        return groups

    def logs_get_messages(self,group_name, stream_name):
        messages = []
        for event in self.logs.get_log_events(logGroupName=group_name, logStreamName=stream_name).get('events'):
            messages.append(event.get('message'))
        return messages
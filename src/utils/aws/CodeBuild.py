import boto3

from utils.Dev import Dev


class CodeBuild:

    def __init__(self):
        self.codebuild = boto3.client('codebuild')
        return

    def _invoke_via_paginator(self, method, field_id, use_paginator, **kwargs):
        paginator = self.codebuild.get_paginator(method)
        for page in paginator.paginate(**kwargs):
            for id in page.get(field_id):
                yield id
            if use_paginator is False:
                return

    def all_builds_ids(self, use_paginator = False):
        return self._invoke_via_paginator('list_builds','ids',use_paginator)

    def project_builds(self,ids):
        return self.codebuild.batch_get_builds(ids=ids)

    def project_create(self, **kvargs):
        return self.codebuild.create_project(**kvargs)

    def project_delete(self, project_name):
        if project_name not in self.projects():
            return False
        self.codebuild.delete_project(name=project_name)
        if project_name not in self.projects():
            return True


    def project_info(self, project_name):
        return self.codebuild.batch_get_projects(names=[project_name])

    def project_builds_ids(self, project_name, use_paginator=False):
        if use_paginator:
            kwargs = { 'projectName' : project_name }
        else:
            kwargs = { 'projectName' : project_name ,
                       'sortOrder'   : 'DESCENDING'  }
        return self._invoke_via_paginator('list_builds_for_project', 'ids',use_paginator, **kwargs)


    def projects(self):
        return self.codebuild.list_projects().get('projects')

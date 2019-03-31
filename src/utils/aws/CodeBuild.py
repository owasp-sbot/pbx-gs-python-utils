import boto3

from utils.Dev import Dev
from utils.Misc import Misc


class CodeBuild:

    def __init__(self, project_name):
        self.codebuild    = boto3.client('codebuild')
        self.project_name = project_name
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

    def build_details(self, build_id):
        return self.codebuild.batch_get_builds(ids=[build_id])

    def build_start(self):
        kvargs = { 'projectName': self.project_name }
        return self.codebuild.start_build(**kvargs).get('build').get('arn')

    def project_builds(self,ids):
        return self.codebuild.batch_get_builds(ids=ids)

    def project_create(self, project_repo, service_role):

        kvargs = {
            'name': self.project_name,
            'source': {'type': 'GITHUB',
                       'location': project_repo},
            'artifacts': {'type': 'NO_ARTIFACTS'},
            'environment': {'type': 'LINUX_CONTAINER',
                            'image': 'aws/codebuild/python:3.7.1-1.7.0',
                            'computeType': 'BUILD_GENERAL1_SMALL'},
            'serviceRole': service_role
        }

        return self.codebuild.create_project(**kvargs)

    def project_delete(self):
        if self.project_exists() is False: return False
        self.codebuild.delete_project(name=self.project_name)
        return self.project_exists() is False

    def project_exists(self):
        return self.project_name in self.projects()


    def project_info(self, project_name):
        projects = Misc.get_value(self.codebuild.batch_get_projects(names=[project_name]),'projects',[])
        return Misc.array_pop(projects,0)

    def project_builds_ids(self, project_name, use_paginator=False):
        if use_paginator:
            kwargs = { 'projectName' : project_name }
        else:
            kwargs = { 'projectName' : project_name ,
                       'sortOrder'   : 'DESCENDING'  }
        return self._invoke_via_paginator('list_builds_for_project', 'ids',use_paginator, **kwargs)


    def projects(self):
        return self.codebuild.list_projects().get('projects')

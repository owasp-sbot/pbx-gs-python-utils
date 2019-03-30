from unittest import TestCase

from utils.Assert        import Assert
from utils.Dev import Dev
from utils.aws.CodeBuild import CodeBuild


class Test_CodeBuild(TestCase):

    def setUp(self):
        self.code_build = CodeBuild()

    def test_all_builds_ids(self):                      # LONG running test
        ids = list(self.code_build.all_builds_ids())
        Assert(ids).size_is(100)
        ids = list(self.code_build.all_builds_ids(use_paginator=True))
        Assert(ids).is_bigger_than(1000)

    def test_project_builds(self):
        ids = list(self.code_build.project_builds_ids('GSBot_code_build'))
        assert len(self.code_build.project_builds(ids[0:2])) == 3

    def test_project_builds_ids(self):                  # LONG running test
        assert len(list(self.code_build.project_builds_ids('GSBot_code_build'             )))  > 20
        assert len(list(self.code_build.project_builds_ids('pbx-group-security-site'      ))) == 100
        assert len(list(self.code_build.project_builds_ids('GSBot_code_build'       , True)))  > 20
        assert len(list(self.code_build.project_builds_ids('pbx-group-security-site', True)))  > 1200


    def test_project_create__project_delete(self):
        project_name = 'Code_Build_Test'
        project_repo = 'https://github.com/pbx-gs/gsbot-build'
        service_role = 'arn:aws:iam::244560807427:role/service-role/gsbot-code-build-service'

        kvargs = {
            'name'       : project_name,
            'source'     : { 'type'       : 'GITHUB',
                             'location'   :  project_repo                           }               ,
            'artifacts'  : { 'type'       : 'NO_ARTIFACTS'                          },
            'environment': { 'type'       : 'LINUX_CONTAINER'                        ,
                             'image'      : 'aws/codebuild/python:3.7.1-1.7.0'       ,
                             'computeType': 'BUILD_GENERAL1_SMALL'                  },
            'serviceRole': service_role
        }
        try:
            result = self.code_build.project_create(**kvargs)
            project     = result.get('project')
            project_arn = project.get('arn')
            assert project_name in project_arn
        except Exception as error:
            Dev.pprint(error)

        assert self.code_build.project_delete(project_name) is True

    def test_project_info(self):
        Dev.pprint(self.code_build.project_info('GSBot_code_build' ))

    def test_projects(self):
        result = self.code_build.projects()
        Assert(result).is_bigger_than(2).is_smaller_than(100)



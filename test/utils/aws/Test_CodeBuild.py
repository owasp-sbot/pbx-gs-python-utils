from unittest               import TestCase
from utils.Assert           import Assert
from utils.Dev              import Dev
from utils.aws.CodeBuild    import CodeBuild

delete_on_teardown = False
project_name       = 'Code_Build_Test'
project_repo       = 'https://github.com/pbx-gs/gsbot-build'
service_role       = 'arn:aws:iam::244560807427:role/service-role/gsbot-code-build-service'
project_arn        = 'arn:aws:codebuild:eu-west-2:244560807427:project/Code_Build_Test'

class Test_CodeBuild(TestCase):

    @classmethod
    def setUpClass(cls):
        code_build = CodeBuild(project_name)
        if code_build.project_exists() is False:
            assert code_build.project_exists() is False
            code_build.project_create(project_repo, service_role)

    @classmethod
    def tearDownClass(cls):
        code_build = CodeBuild(project_name)
        assert code_build.project_exists() is True

        if delete_on_teardown:
            code_build.project_delete()
            assert code_build.project_exists() is False

    def setUp(self):
        self.code_build = CodeBuild(project_name)

    def test_all_builds_ids(self):                      # LONG running test
        ids = list(self.code_build.all_builds_ids())
        Assert(ids).size_is(100)
        ids = list(self.code_build.all_builds_ids(use_paginator=True))
        Assert(ids).is_bigger_than(1000)

    def test_build_start(self):
        build_id = self.code_build.build_start()
        Dev.pprint(build_id)
        build_details = self.code_build.build_details(build_id)
        Dev.pprint(build_details)


    def test_project_builds(self):
        ids = list(self.code_build.project_builds_ids('GSBot_code_build'))
        assert len(self.code_build.project_builds(ids[0:2])) == 3

    def test_project_builds_ids(self):                  # LONG running test
        assert len(list(self.code_build.project_builds_ids('GSBot_code_build'             )))  > 20
        assert len(list(self.code_build.project_builds_ids('pbx-group-security-site'      ))) == 100
        assert len(list(self.code_build.project_builds_ids('GSBot_code_build'       , True)))  > 20
        assert len(list(self.code_build.project_builds_ids('pbx-group-security-site', True)))  > 1200

    def test_project_info(self):
        project = self.code_build.project_info(project_name)
        (
            Assert(project).field_is_equal('arn'        , project_arn )
                           .field_is_equal('name'       , project_name)
                           .field_is_equal('serviceRole', service_role)
        )

    def test_projects(self):
        result = self.code_build.projects()
        Assert(result).is_bigger_than(2).is_smaller_than(100)



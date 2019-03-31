from time import sleep
from unittest               import TestCase
from utils.Assert           import Assert
from utils.Dev              import Dev
from utils.aws.CodeBuild    import CodeBuild
from utils.aws.IAM import IAM

delete_on_setup    = False
delete_on_teardown = False
account_id         = '244560807427'
project_name       = 'Code_Build_Test'
project_repo       = 'https://github.com/pbx-gs/gsbot-build'
service_role       = 'arn:aws:iam::{0}:role/Code_Build_Test'.format(account_id)
#service_role_2     = 'arn:aws:iam::244560807427:role/service-role/gsbot-code-build-service'
project_arn        = 'arn:aws:codebuild:eu-west-2:{0}:project/Code_Build_Test'.format(account_id)
assume_policy      = {'Statement': [ { 'Action': 'sts:AssumeRole',
                                                 'Effect': 'Allow',
                                                 'Principal': { 'Service': 'codebuild.amazonaws.com'}}]}

#CodeBuildBasePolicy-GSBot_code_build-eu-west-2
class Test_CodeBuild(TestCase):

    @classmethod
    def setUpClass(cls):
        code_build = CodeBuild(project_name=project_name, role_name=project_name)
        iam        = IAM(role_name=project_name)
        if delete_on_setup:
            code_build.project_delete()
            iam.role_delete()
        if code_build.project_exists() is False:
            assert code_build.project_exists() is False
            iam.role_create(assume_policy)                                # create role
            assert iam.role_info().get('Arn') == service_role             # confirm the role exists
            sleep(1)
            code_build.project_create(project_repo, service_role)         # in a non-deterministic way, this sometimes throws the error: CodeBuild is not authorized to perform: sts:AssumeRole

    @classmethod
    def tearDownClass(cls):
        code_build = CodeBuild(project_name=project_name,role_name=project_name)
        iam        = IAM(role_name=project_name)
        assert code_build.project_exists() is True
        assert iam.role_exists()           is True
        if delete_on_teardown:
            code_build.project_delete()
            iam       .role_delete()
            assert code_build.project_exists() is False
            assert iam.role_exists()           is False

    def setUp(self):
        self.code_build = CodeBuild(project_name=project_name,role_name=project_name)
        self.iam        = IAM(role_name=project_name)

    def test_all_builds_ids(self):                      # LONG running test
        ids = list(self.code_build.all_builds_ids())
        Assert(ids).size_is(100)
        ids = list(self.code_build.all_builds_ids(use_paginator=True))
        Assert(ids).is_bigger_than(1000)

    def test_build_start(self):
        # policies = [ 'arn:aws:iam::244560807427:policy/service-role/CodeBuildBasePolicy-GSBot_code_build-eu-west-2',
        #              'arn:aws:iam::244560807427:policy/service-role/CodeBuildCloudWatchLogsPolicy-GSBot_code_build-eu-west-2',
        #              'arn:aws:iam::aws:policy/CloudWatchFullAccess']
        # self.iam.role_policies_attach(policies)
        # #Dev.pprint(self.iam.role_policies())
        self.code_build.policies_create()
        #return
        build_id     = self.code_build.build_start()
        build_info   = self.code_build.build_wait_for_completion(build_id,1, 60)
        build_phases = build_info.get('phases')

        phase        = build_phases.pop(-2)

        Dev.pprint(phase.get('phaseType'),phase.get('phaseStatus'),phase.get('contexts')[0].get('message') )


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



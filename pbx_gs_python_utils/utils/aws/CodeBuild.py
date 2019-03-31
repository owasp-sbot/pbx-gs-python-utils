import  boto3
from    time                                import sleep
from    pbx_gs_python_utils.utils.Dev       import Dev
from    pbx_gs_python_utils.utils.Misc      import Misc
from    pbx_gs_python_utils.utils.aws.IAM   import IAM


class CodeBuild:

    def __init__(self, project_name, role_name):
        self.codebuild    = boto3.client('codebuild')
        self.iam          = IAM(role_name=role_name)
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

    def build_info(self, build_id):
        builds = self.codebuild.batch_get_builds(ids=[build_id]).get('builds')
        return Misc.array_pop(builds,0)

    def build_start(self):
        kvargs = { 'projectName': self.project_name }
        return self.codebuild.start_build(**kvargs).get('build').get('arn')

    def build_wait_for_completion(self, build_id, sleep_for=0.5, max_attempts=20):
        for i in range(0,max_attempts):
            build_info    = self.build_info(build_id)
            build_status  = build_info.get('buildStatus')
            current_phase = build_info.get('currentPhase')
            Dev.pprint("[{0}] {1} {2}".format(i,build_status,current_phase))
            if build_status != 'IN_PROGRESS':
                return build_info
            sleep(sleep_for)
        return None


    def policies_create(self):
        policies = {
            "CodeBuildBasePolicy" : {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Resource": [
                                    "arn:aws:logs:eu-west-2:244560807427:log-group:/aws/codebuild/GSBot_code_build",
                                    "arn:aws:logs:eu-west-2:244560807427:log-group:/aws/codebuild/GSBot_code_build:*"
                                ],
                                "Action": [
                                    "logs:CreateLogGroup",
                                    "logs:CreateLogStream",
                                    "logs:PutLogEvents"
                                ]
                            },
                            {
                                "Effect": "Allow",
                                "Resource": [
                                    "arn:aws:s3:::codepipeline-eu-west-2-*"
                                ],
                                "Action": [
                                    "s3:PutObject",
                                    "s3:GetObject",
                                    "s3:GetObjectVersion",
                                    "s3:GetBucketAcl",
                                    "s3:GetBucketLocation"
                                ]
                            }
                        ]
                    },
            "Cloud_Watch_Policy": {
                                      "Version": "2012-10-17",
                                      "Statement": [
                                        {
                                          "Sid": "CloudWatchLogsPolicy",
                                          "Effect": "Allow",
                                          "Action": [
                                            "logs:CreateLogGroup",
                                            "logs:CreateLogStream",
                                            "logs:PutLogEvents"
                                          ],
                                          "Resource": [
                                            "*"
                                          ]
                                        },
                                        {
                                          "Sid": "CodeCommitPolicy",
                                          "Effect": "Allow",
                                          "Action": [
                                            "codecommit:GitPull"
                                          ],
                                          "Resource": [
                                            "*"
                                          ]
                                        },
                                        {
                                          "Sid": "S3GetObjectPolicy",
                                          "Effect": "Allow",
                                          "Action": [
                                            "s3:GetObject",
                                            "s3:GetObjectVersion"
                                          ],
                                          "Resource": [
                                            "*"
                                          ]
                                        },
                                        {
                                          "Sid": "S3PutObjectPolicy",
                                          "Effect": "Allow",
                                          "Action": [
                                            "s3:PutObject"
                                          ],
                                          "Resource": [
                                            "*"
                                          ]
                                        }
                                      ]
                                    }
                , "Access_Secret_Manager": {
                                                "Version": "2012-10-17",
                                                "Statement": [
                                                    {
                                                        "Sid": "VisualEditor0",
                                                        "Effect": "Allow",
                                                        "Action": [
                                                            "secretsmanager:GetResourcePolicy",
                                                            "secretsmanager:GetSecretValue",
                                                            "secretsmanager:DescribeSecret",
                                                            "secretsmanager:ListSecretVersionIds"
                                                        ],
                                                        "Resource": "arn:aws:secretsmanager:*:*:secret:*"
                                                    }
                                                ]
                                            },
                "Invoke_Lambda_Functions": {
                                                "Version": "2012-10-17",
                                                "Statement": [
                                                    {
                                                        "Sid": "VisualEditor0",
                                                        "Effect": "Allow",
                                                        "Action": "lambda:InvokeFunction",
                                                        "Resource": "arn:aws:lambda:*:*:function:*"
                                                    }
                                                ]
                                            },
                "Create_Update_Lambda_Functions": {
                                                "Version": "2012-10-17",
                                                "Statement": [
                                                    {
                                                        "Sid": "VisualEditor0",
                                                        "Effect": "Allow",
                                                        "Action": ["lambda:ListFunctions","lambda:GetFunction","lambda:CreateFunction","lambda:UpdateFunctionCode"],
                                                        "Resource": "arn:aws:lambda:*:*:function:*"
                                                    }
                                                ]
                                            },
                "Pass_Role": {
                                "Version": "2012-10-17",
                                "Statement": [{
                                    "Effect": "Allow",
                                    "Action": [
                                        "iam:GetRole",
                                        "iam:PassRole"
                                    ],
                                    "Resource": "arn:aws:iam::244560807427:role/lambda_with_s3_access"
                                }]
                            }
            }
        role_policies = list(self.iam.role_policies().keys())
        for base_name, policy in policies.items():
            policy_name = "{0}-{1}".format(base_name, self.project_name)
            if policy_name in role_policies:
                continue
            if self.iam.policy_info(policy_name) is None:
                self.iam.policy_create(policy_name, policy)
            policy_arn = self.iam.policy_info(policy_name).get('Arn')
            Dev.pprint(policy_arn)
            self.iam.role_policies_attach(policy_arn)

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


    def project_info(self):
        projects = Misc.get_value(self.codebuild.batch_get_projects(names=[self.project_name]),'projects',[])
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

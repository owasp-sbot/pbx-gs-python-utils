from pbx_gs_python_utils.utils.Misc import Misc
from osbot_aws.apis.CodeBuild import CodeBuild


def run(event, context):
    project_name = 'Code_Build_Test'
    build_id     = CodeBuild(project_name=project_name,role_name=project_name).build_start()
    return {
        'headers': {'Content-Type': 'application/json'},
        "statusCode": 200,
        "body": Misc.json_format({'build_id': build_id})
    }
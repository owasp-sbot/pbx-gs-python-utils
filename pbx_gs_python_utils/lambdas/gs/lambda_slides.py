from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk
from pbx_gs_python_utils.utils.aws.Lambdas import load_dependency


def run(event, context):
    try:
        load_dependency("gmail")
        load_dependency("elastic-slack")                                                    # load dependency (download and unzip if first run)
        from pbx_gs_python_utils.gsuite.handlers.Lambda_Slides import Lambda_Slides         # import Lambda_Slides class
        return Lambda_Slides().handle_lambda_event(event)                                   # invoke lambda handler from Lambda_Slides class

        #return "200 OK"

    except Exception as error:
        message = "[lambda_slides] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
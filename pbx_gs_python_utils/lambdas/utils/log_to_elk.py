def run(event, context):

    from pbx_gs_python_utils.utils.aws.Lambdas import load_dependency
    load_dependency('elastic')

    from pbx_gs_python_utils.utils.Log_To_Elk import log_info,log_debug,log_error

    try:
        level    = event.get('level'   )
        category = event.get('category')
        message  = event.get('message' )
        data     = event.get('data'    )
        index    = event.get('index'   )

        if message:
            if level == 'info':
                return log_info (message, category, data, index)
            elif level == 'debug':
                return log_debug(message, category, data, index)
            elif level == 'error':
                return log_error(message, category, data, index)
            else:
                return log_error("Error: not supported error level: {0} \n\nmessage: {1}\ncategory: {2}\ndata: {3}".format(level, message, category, data))

    except Exception as error:
        return log_error('Error: ' + str(error), 'Lambda.utils.log_to_elk')

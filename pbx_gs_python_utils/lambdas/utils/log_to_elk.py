def run(event, context):
    from osbot_aws.apis.Lambda import load_dependency
    load_dependency('elastic')

    from pbx_gs_python_utils.utils.Log_To_Elk import Log_To_Elk

    try:

        log_to_elk = Log_To_Elk()
        level    = event.get('level'   )
        category = event.get('category')
        message  = event.get('message' )
        data     = event.get('data'    )
        index    = event.get('index'   )
        if message:
            if level == 'info':
                return log_to_elk.log_info (message=message, category=category, data=data, index=index)
            elif level == 'debug':
                return log_to_elk.log_debug(message=message, category=category, data=data, index=index)
            elif level == 'error':
                return log_to_elk.log_error(message=message, category=category, data=data, index=index)
            else:
                return log_to_elk.log_error("Error: not supported error level: {0} \n\nmessage: {1}\ncategory: {2}\ndata: {3}".format(level, message, category, data))
        return message
    except Exception as error:
        return log_to_elk.log_error('Error: ' + str(error), 'Lambda.utils.log_to_elk')

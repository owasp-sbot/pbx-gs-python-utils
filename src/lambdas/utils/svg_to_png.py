from utils.aws.Lambdas import Lambdas


def run(event, context):
    request_test = Lambdas('dev.node_phantom')

    if event.get('width') is None:
        event['width'] = 1000
    return request_test.invoke(event)

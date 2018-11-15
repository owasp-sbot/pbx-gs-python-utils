import  datetime
import pprint

from    utils.aws.secrets import Secrets
from    utils.Elastic_Search import Elastic_Search

class Log_To_Elk():
    _elastic_cache = None

    def __init__(self):
        self.index_id     = 'elastic_logs'
        self.port         = 9243
        self.host         = '546a0b2e8f0d4426a2f3337effcfc02a.eu-west-1.aws.found.io'
        self.secret_id    = 'elastic_cloud_test'
        self.elastic      = self.setup()

    def create(self):
        if self.elastic.exists() is False:
            self.elastic.create_index().create_index_pattern()
        return self.elastic.exists()

    def setup(self, index = None):
        if index is None:
            index = self.index_id
        username = 'elastic'
        password = Secrets(self.secret_id).value()
        return Elastic_Search(index)._setup_Elastic_on_cloud(self.host, self.port, username, password)

def log_debug(message, data = None, category='log', index = None): return log_message('debug', message, category, data, index)
def log_error(message, data = None, category='log', index = None): return log_message('error', message, category, data, index)
def log_info (message, data = None, category='log', index = None): return log_message('info' , message, category ,data, index)


def log_message(type, message,category, data ,index):
    if isinstance(data, str):
        data = { "str" : data }                 # data needs to be an object and not a string (since once there is a string in the data field in ELK , string values will throw an exception)

    elastic = Log_To_Elk().setup(index)
    item = { 'level'    : type              ,
             'source'   : 'python_script'   ,
             'category' : category          ,
             'message'  : message           ,
             'data'     : data              ,
             'date'     : datetime.datetime.utcnow()}
    return { "item" : pprint.pformat(item), "elastic_response" : elastic.add(item) }
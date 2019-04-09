
import sys

sys.path.append('..')

print('***** loading dependency')
from osbot_aws.apis.Lambda import load_dependency

load_dependency('elastic')

print('***** done')

from unittest import TestCase

from pbx_gs_python_utils.utils.Dev            import Dev
from pbx_gs_python_utils.utils.Json           import Json
from pbx_gs_python_utils.utils.Elastic_Search import Elastic_Search


class Pytest_To_Elk:

    def __init__(self):
        self.pytest_json   = './report.json'
        self.index_id      = 'pytest_data'
        self.aws_secret_id = 'elastic-logs-server-1'
        self._elastic      = None

    # helper methods
    def elastic(self):
        if self._elastic is None:
            self._elastic = Elastic_Search(index=self.index_id, aws_secret_id= self.aws_secret_id)
        return self._elastic

    # main methods
    def convert_pytest_data(self, pytest_data):

        #Dev.pprint(pytest_data)
        report = pytest_data.get('report')
        elk_data = []
        Dev.pprint(report.get('created_at'))
        created_at = report.get('created_at')

        from datetime import datetime
        date = datetime.strptime('2019-04-02 01:10:36.068552', '%Y-%m-%d %H:%M:%S.%f')       #'2019-04-02 01:10:36.068552'
        date = datetime.now()
        pytest_session = { 'created_at' : date.utcnow()              ,
                           'environment': report.get('environment'  ),
                           'summary'    : report.get('summary'      )}
        elk_data.append(pytest_session)
        return elk_data


    def load_pytest_data(self):
        return Json.load_json(self.pytest_json)

    def send_data_to_elk(self, data, delete_index=False):
        elastic = self.elastic()
        if delete_index:
            elastic.delete_index()
        if elastic.exists() is False:
            elastic.create_index()
        return elastic.add_bulk(data)

    def load_and_send(self):
        pytest_data = self.load_pytest_data()
        elk_data    = self.convert_pytest_data(pytest_data)
        result      = self.send_data_to_elk(elk_data, False)
        Dev.pprint("Sent {0} records to ELK".format(result))

if __name__ == '__main__':
    Pytest_To_Elk().load_and_send()


class Test_Pytest_To_Elk(TestCase):
    def setUp(self):
        self.pytest_to_elk = Pytest_To_Elk()

    def test_load_pytest_data(self):
        assert 'created_at' in list(set(self.pytest_to_elk.load_pytest_data().get('report')))

    def test_convert_pytest_data(self):
        pytest_data = self.pytest_to_elk.load_pytest_data()
        elk_data = self.pytest_to_elk.convert_pytest_data(pytest_data)

        Dev.pprint(elk_data)

    def test_send_data_to_elk(self):
        pytest_data = self.pytest_to_elk.load_pytest_data()
        elk_data = self.pytest_to_elk.convert_pytest_data(pytest_data)
        result = self.pytest_to_elk.send_data_to_elk(elk_data,False)
        Dev.pprint(result)
from unittest import TestCase

from pbx_gs_python_utils.utils.Log_To_Elk import Log_To_Elk


class Test_Log_To_Elk(TestCase):

    def setUp(self):
        self.log_to_elk = Log_To_Elk()

    def test_setup(self):
        assert self.log_to_elk.elastic.index    == 'elastic_logs'
        assert self.log_to_elk.elastic.port     == 9243
        assert self.log_to_elk.elastic.username == 'elastic'

    def test_log_debug(self):
        response = self.log_to_elk.log_debug('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'

    def test_log_info(self):
        response = self.log_to_elk.log_info('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'

    def test_log_error(self):
        response = self.log_to_elk.log_error('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'
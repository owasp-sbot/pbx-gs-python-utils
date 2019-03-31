import unittest

from utils.Dev import Dev
from pbx_gs_python_utils.utils.Elastic_Search import *


class Test_Elastic_Search(unittest.TestCase):

    def setUp(self):
        self.index     = 'jira'
        self.secret_id = 'elastic-jira-dev-2'
        self.elastic = Elastic_Search()._setup_Elastic_on_cloud_via_AWS_Secret(self.index, self.secret_id)


    def test_add_data_with_timestamp(self):
        data    = { 'answer' : 42}
        response = self.elastic.add_data_with_timestamp(data)
        assert response.get("_index") == self.elastic.index


    def test_search_using_query(self):
        term = 'jira'
        query =  {"query": { "wildcard": { "Summary": term}}}
        result = list(self.elastic.search_using_query(query))

        assert term in result.pop(0)['Summary'].lower()
        assert len(result) > 20


    def test_test_search_using_query___large_query(self):
        query = {"_source": ["Key", "Issue Links"], }

        result = list(self.elastic.set_index('sec_project').search_using_query(query))
        Dev.pprint(len(result))

    def test_get_data_between_dates(self):
        results = self.elastic.get_data_between_dates("Created", "now-1d", "now")
        Dev.pprint(len(results))
        for issue in results:
            print(issue.get('Summary'))


    def test_index_list(self):
        assert 'jira' in self.elastic.index_list()

    def test_search_using_lucene(self):
        #query = "Summary:jira"
        query = 'Project:RISK AND Status:"Fixed"'
        self.index = "*"
        results = list(self.elastic.search_using_lucene(query))

        #for issue in results:
        #    print('{0:10} {1:10} {2:20} {3}'.format(issue.get('Key'), issue.get('Project'),issue.get('Status'),issue.get('Summary')))

        assert len(results) > 100

    def test_search_using_lucene____Issue_with_Epic(self):
        self.elastic.index = 'it_assets'
        query = '"GSOKR-924"'
        results = list(self.elastic.search_using_lucene(query))
        assert len(results) == 25

if __name__ == '__main__':
    unittest.main()

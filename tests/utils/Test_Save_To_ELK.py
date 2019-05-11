import datetime
import unittest
from time import sleep
from unittest import TestCase

from utils.Dev import Dev
from utils.Save_To_ELK import Save_To_ELK


class Test_Save_To_ELK(TestCase):
    def setUp(self):
        self.save_to_elk = Save_To_ELK()
        self.elastic     = self.save_to_elk.elastic
        self.doc_type    = 'unit-test'

    def test___init__(self):
        self.elastic.create_index()
        assert 'save_to_elk' in self.elastic.index_list()


    def test_add_document(self):
        test_doc = { "answer" : 42, "source" : "from_unit_test", "now": str(datetime.datetime.utcnow())}
        doc_type = 'unit-test'
        response = self.save_to_elk.add_document(doc_type, test_doc)
        #Dev.pprint(data)
        #Dev.pprint(response)
        return test_doc

    def test_get_most_recent_version_of_document(self):
        test_doc = self.test_add_document()
        sleep(1)            # give ES time to index it
        lucene_query = "doc_data.source:from_unit_test"
        match = self.save_to_elk.get_most_recent_version_of_document(lucene_query)
        assert match == test_doc

    def test_find_document_by_type(self):
        data = self.save_to_elk.find_documents_of_type(self.doc_type)
        #Dev.pprint(data)
        assert len(data) > 0

    @unittest.SkipTest
    def test_delete_documents_with_id(self):
        id = "9QckDmcByR-UEnoIswj8"
        result = self.save_to_elk.delete_documents_with_id(id)
        Dev.pprint(result)

    def test_delete_documents_with_type(self):
        self.save_to_elk.delete_documents_with_type(self.doc_type)


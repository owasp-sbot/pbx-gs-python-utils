import  json
import  datetime
import  requests

from    elasticsearch                           import Elasticsearch, helpers, NotFoundError
from osbot_aws.apis.Secrets import Secrets
from    requests.auth                           import HTTPBasicAuth
from    pbx_gs_python_utils.utils.Http          import PUT, DELETE
#note the max query value in the search has been increased from 10000 to 100000 (which will need to be done on any new ES Install)
# PUT _all/_settings
# {
# "index.max_result_window" : "100000"
# }



class Elastic_Search:
    def __init__(self, index = 'iis-logs-', aws_secret_id = None):
        self.timestamp      = datetime.datetime.utcnow()
        self.index          = index
        self._setup_Elastic_on_localhost()                  # default to localhost
        self._setup_Elastic_on_localhost()                  # default to localhost
        self._result        = None

        if index and aws_secret_id:
            self._setup_Elastic_on_cloud_via_AWS_Secret(index, aws_secret_id)

    def _setup_Elastic_on_localhost(self):
        self.host   = 'localhost'
        self.port   = 9200
        self.scheme = 'http'
        self.es     = Elasticsearch([{'host': self.host, 'port': self.port}])

    def _setup_Elastic_on_cloud_via_AWS_Secret(self,index, secret_id):
        credentials = json.loads(Secrets(secret_id).value())
        host        = credentials['host']
        username    = credentials['username']
        password    = credentials['password']
        port        = credentials['port']
        self.index  = index
        self._setup_Elastic_on_cloud(host, port, username, password)
        return self

    def _setup_Elastic_on_cloud(self, host, port, username, password):
        self.host     = host
        self.port     = port
        self.username = username
        self.password = password
        self.scheme   = 'https'
        self.es       = Elasticsearch([host], http_auth=(username, password),scheme="https", port=port)
        return self


    def add_data_with_timestamp(self,data):
        data["@timestamp"] = self.timestamp
        return self.es.index(index=self.index, doc_type='item', body=data)

    def add(self,data, id_key = None):
        try:
            if id_key is not None:
                return self.es.index(index=self.index, doc_type='item', body=data, id=data[id_key])
            else:
                return self.es.index(index=self.index, doc_type='item', body=data)
        except Exception as error:
            print(error)
            return {"elk-error": "{0}".format(error)}

    def add_bulk(self, data, id_key = None, pipeline = None):
        ok = 0
        if data:
            actions = []
            for item in data:
                item_data = {
                                "_index": self.index,
                                "_type": 'item',
                                "_source": item,
                            }
                if id_key is not None:
                    item_data["_id"] = item[id_key]
                actions.append(item_data)

            if pipeline is None:
                ok, _ = helpers.bulk(self.es, actions, index=self.index)
            else:
                ok, _ = helpers.bulk(self.es, actions, index=self.index, pipeline=pipeline)
        return ok

    def create_index(self,body = {}):
        if self.exists() is False:
            self._result = self.es.indices.create(index=self.index, body=body)
        return self

    def create_index_with_location_geo_point(self,field = "location"):
        body = {
                "mappings": {
                    "item": {
                        "properties": {
                            field: {
                                "type": "geo_point"
                            }
                        }
                    }
                }
            }
        self.create_index(body)
        return self

    def create_index_pattern(self, add_time_field = True):
        if add_time_field:
            payload = {
                "type": "index-pattern",
                "index-pattern": {"title": self.index + '*', "timeFieldName": "date"}
            }
        else:
            print('creating index without index pattern')
            payload = {
                "type": "index-pattern",
                "index-pattern": {"title": self.index + '*'}
            }
        data = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}

        if self.host == 'localhost':
            url = 'http://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host, self.port, self.index)
            self._result = json.loads(PUT(url, data, headers))

        else:
            url = 'https://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host, self.port, self.index)
            response = requests.put(url, data, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
            self._result = json.loads(response.text)

        return self

    def delete_index_pattern(self):
        try:
            if self.host == 'localhost':
                url = 'http://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host,self.port, self.index)
                self._result = json.loads(DELETE(url))
            else:
                url = 'https://{0}:{1}/.kibana/doc/index-pattern:{2}'.format(self.host, self.port, self.index)
                response = requests.delete(url, auth=HTTPBasicAuth(self.username, self.password))
                self._result = json.loads(response.text)
        except Exception as error:
            self._result = { 'error':  error}
        return self

    def delete_data_by_id(self, id):
        return self.es.delete(index=self.index, doc_type='item', id=id)

    def get_data(self,id):
        try:
            return self.es.get(index=self.index, doc_type='item', id=id)
        except NotFoundError:
            return None

    def get_many(self, ids):
        data = self.es.mget(index=self.index, doc_type='item', body={'ids': ids})
        results = {}
        for item in data['docs']:
            _id = item['_id']
            if item['found'] is False:
                results[_id] = None
            else:
                results[_id] = item['_source']
        return results

    def get_data_First_10(self):
        results = self.es.search(index=self.index, body={"query": {"match_all": {}}})
        for result in results['hits']['hits']:
            yield result['_source']

    def get_index_settings(self):
        url = 'https://{3}:{4}@{0}:{1}/{2}/_settings'.format(self.host, self.port, self.index, self.username, self.password)
        return json.loads(requests.get(url).text)

    def get_data_between_dates(self,field, from_date,to_date):
        query = {"query": { "range": { field: { "gte": from_date,
                                                "lt" : to_date     } }}}
        return list(self.search_using_query(query))

    def search_using_lucene(self, query, size=100000, sort = None):              # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        results = self.es.search(index=self.index, q=query, size=size,sort = sort)
        for result in results['hits']['hits']:
            yield result['_source']

    def search_using_lucene_index_by_id(self, query, size=100000, sort = None):  # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        elk_results = self.es.search(index=self.index, q=query, size=size, sort= sort)
        results = {}
        for result in elk_results['hits']['hits']:
            id          = result['_id']
            value       = result['_source']
            results[id] = value
        return results

    def search_using_lucene_sort_by_date(self, query, size=100000):              # for syntax and examples of lucene queries see https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-query-string-query.html#query-string-syntax
        query = query.replace('“', '"').replace('”','"')                        # fix the quotes we receive from Slack
        elk_results = self.es.search(index=self.index, q=query, size=size, sort= "date:desc")
        results = []
        for result in elk_results['hits']['hits']:
            id          = result['_id']
            value       = result['_source']
            item        = { "id":id , "value": value}
            results.append(item)
        return results

    def search_using_query(self, query, size = 100000):
        results = self.es.search(index=self.index, body= query, size=size)
        for result in results['hits']['hits']:
            yield result['_source']

    def search_on_field_for_value(self, field, value, size=10000):
        query = {"query": {"match": { field : {"query": value}}}}
        return self.search_using_query(query, size=size)

    def search_on_field_for_values(self, field, values):
        query = {"query": { "constant_score": { "filter": { "terms": { field: values } } } } }
        return self.search_using_query(query)

    # this is not working
    # def search_get_unique_field_values(self, field,size = 10000):
    #     query = {
    #         "size": 0,
    #         "aggs": {
    #             "unique_ids": {
    #                 "terms": {
    #                     "field": 'field',
    #                     "size": size
    #                 }
    #             }
    #         }
    #     }
    #     return self.search_using_query(query)


    def set_index_settings(self, settings):
        headers = {'Content-Type': 'application/json'}
        url = 'https://{0}:{1}/{2}/_settings'.format(self.host, self.port, self.index)
        response = requests.put(url, json.dumps(settings), headers=headers, auth=HTTPBasicAuth(self.username, self.password))
        return response.text

    def set_index_settings_total_fields(self,value):
        self.set_index_settings({"index.mapping.total_fields.limit": value})
        return self

    def delete_using_query(self, query):
        results = self.es.delete_by_query(index=self.index, body=query)
        return results

    def delete_index(self):
        if self.exists():
            self._result = self.es.indices.delete(self.index)
        return self

    def index_list(self):
        return set(self.es.indices.get_alias())

    def exists(self):
        return self.es.indices.exists(self.index)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        return self

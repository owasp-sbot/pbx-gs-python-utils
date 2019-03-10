import requests

from utils.Dev import Dev
from utils.Misc import Misc
from utils.aws.secrets import Secrets


class API_Jira_Rest:
    def __init__(self):
        self.secrets_id = 'GS_BOT_GS_JIRA'
        self._config    = None

    def config(self):
        if self._config is None:
            data = Secrets(self.secrets_id).value_from_json_string()
            self._config = (data.get('server'), data.get('username'), data.get('password'))
        return self._config

    def request_get(self,path):
        (server, username, password)= self.config()
        path = '{0}/rest/api/2/{1}'.format(server, path)
        response = requests.get(path, auth=(username, password))
        if response.status_code == 200:
            return response.text
        Dev.pprint('[Error][request_get]: {0}'.format(response.text))
        return None

    def request_put(self, path, data):
        json_data = Misc.json_dumps(data)
        (server, username, password) = self.config()
        path = '{0}/rest/api/2/{1}'.format(server, path)
        headers = {'Content-Type': 'application/json'}
        response = requests.put(path, json_data, headers=headers, auth=(username, password))
        if 200 <= response.status_code < 300:
            return True
        Dev.pprint('[Error][request_put]: {0}'.format(response.text))
        return False

    def fields(self):
        return Misc.json_load(self.request_get('field'))

    def fields_by_id(self):
        fields = {}
        for field in Misc.json_load(self.request_get('field')):
            fields[field.get('id')] = field
        return fields

    def fields_by_name(self):
        fields = {}
        for field in Misc.json_load(self.request_get('field')):
            fields[field.get('name')] = field
        return fields

    def issue(self,issue_id):
        path = 'issue/{0}'.format(issue_id)
        data = self.request_get(path)
        return Misc.json_load(data)

    def issue_update_field(self, issue_id, field,value):
        #path = 'issue/{0}'.format(issue_id)
        #data = { "update" : { field :  [{"set" : value} ] }}
        #return self.request_put(path, data)
        return self.issue_update_fields(issue_id, {field:value})

    def issue_update_fields(self, issue_id, fields):
        path = 'issue/{0}'.format(issue_id)
        data = { "update" : {}}
        fields_by_name = self.fields_by_name()
        for key,value in fields.items():
            #if key == 'Rating': key = 'Risk Rating'     # move to special resolver method (needed because 'Risk Rating' was mapped as 'Rating' in ELK)
            field = fields_by_name.get(key)
            if field:
                field_id    = field.get('id')
                schema_type = field.get('schema').get('type')

                if   schema_type == 'option'   : data['update'][field_id] =[{"set": {'value': value }}]
                elif schema_type == 'string'   : data['update'][field_id] = [{"set": value}]
                elif schema_type == 'array'    : data['update'][field_id] = [{"set": value.split(',')}]
                elif schema_type == 'user'     : data['update'][field_id] = [{"set": {'name': value }}]
                else                           : data['update'][field_id] = [{"set": value}]

                #Dev.pprint(field)issue_update
        if len(set(data)) == 0:
            return False
            Dev.pprint(data)
        return self.request_put(path, data)


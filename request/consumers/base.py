from http.client import HTTPSConnection
from tabulate import tabulate
from urllib.parse import urlencode

class Consumer(object):
    def __init__(self, key):
        self.key = key
        self.host = config.host
        self.app_base_route = ''

    def make_request(self, path, query=None, body=None):
        connection = HTTPSConnection(self.host, context=ssl._create_unverified_context())
        params = ''
        if query is not None:
            params = '?{}'.format(urlencode(query))
        path = '{}/{}/{}/{}'.format(
            self.app_base_route,
            self.key,
            method,
            params,
        )
        connection.request('GET', path, body=body)
        response = connection.getresponse()
        data = response.read()
        try:
            return json.loads(data.decode('utf-8'))
        except:
            return {}

    def print_objects(self, objs, fields, cls=None):
        if cls is not None:
            objs = [cls(**o) for o in objs]
        rows = []
        for obj in objs:
            row = []
            for field in fields:
                val = None
                try:
                    row.append(getattr(obj, field))
                except:
                    row.append('-')
            rows.append(row)
        print(tabulate(rows, headers=fields))

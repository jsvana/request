import requests
import json
import sys
from tabulate import tabulate
from urllib.parse import urlencode

from ..config import host

class Consumer(object):
    def __init__(self, key):
        self.key = key
        self.host = host
        self.app_base_route = ''

    def make_request(self, method, query=None, body=None):
        payload = ''
        if query is not None:
            payload = query
        try:
            r = requests.get('https://{}/{}/{}/{}'.format(
                self.host,
                self.app_base_route,
                self.key,
                method,
            ), params=payload)
        except:
            sys.exc_info()[0]

        try:
            return r.json()
        except:
            sys.exc_info()[0]

    def print_objects(self, objs, fields, cls=None, reverse=False):
        """Print a set of objects and allow for some fancy mumbo-jumbo"""
        if cls is not None:
            objs = [cls(**o) for o in objs]
        rows = []
        for obj in objs:
            row = []
            if isinstance(fields, dict):
                for field, transform in fields.items():
                    # Default to identity for transform
                    if transform is None:
                        transform = lambda f: f

                    if isinstance(obj, dict):
                        if field in obj:
                            val = transform(obj[field])
                        else:
                            val = '-'
                    else:
                        try:
                            val = getattr(obj, field)
                        except AttributeError:
                            val = '-'
                    row.append(val)
            else:
                for field in fields:
                    try:
                        row.append(getattr(obj, field))
                    except:
                        row.append('-')
            rows.append(row)

        # Don't print anything if there is nothing to print
        if not rows:
            return

        if reverse:
            rows = reversed(rows)
        print(tabulate(rows, headers=fields))

    def help(self, args):
        """Base help method. Should be overridden by children"""
        print('No commands available for this consumer')

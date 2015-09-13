import argparse
import http.client
import json
from tabulate import tabulate
import urllib.parse
import ssl

import config
from media import Movie

def parse_args():
    parser = argparse.ArgumentParser()
    # TODO(jsvana): move to logger
    # parser.add_argument(
        # '-v', '--verbose',
        # action='store_true',
        # help='print more output',
    # )
    type_args = argparse.ArgumentParser(add_help=False)
    type_args.add_argument(
        '--type',
        choices=['movie'],
        default='movie',
        help='type of media to search for (default is %(default)s',
    )
    subparsers = parser.add_subparsers()
    search_parser = subparsers.add_parser(
        'search',
        parents=[type_args],
        help='search for a given media object',
    )
    search_parser.add_argument(
        'query',
        help='query term to search for',
    )
    search_parser.set_defaults(function=search)

    add_parser = subparsers.add_parser(
        'add',
        parents=[type_args],
        help='add a given media object by id',
    )
    add_parser.add_argument(
        'id',
        help='ID of media to add',
    )
    add_parser.set_defaults(function=add)

    return parser.parse_args()

class Api(object):
    def __init__(self, key):
        self.key = key
        self.host = config.host
        self.app_base_route = ''

    def make_request(self, method, query=None):
        connection = http.client.HTTPSConnection(self.host, context=ssl._create_unverified_context())
        params = ''
        if query is not None:
            params = '?{}'.format(urllib.parse.urlencode(query))
        path = '{}/{}/{}/{}'.format(
            self.app_base_route,
            self.key,
            method,
            params,
        )
        connection.request('GET', path)
        response = connection.getresponse()
        data = response.read()
        try:
            return json.loads(data.decode('utf-8'))
        except:
            return {}

class CouchpotatoApi(Api):
    def __init__(self, key):
        super().__init__(key)
        self.app_base_route = '/couchpotato/api'

    def search(self, query):
        """Search for given movie title"""
        return self.make_request('search', {
            'q': query,
        })

    def add(self, imdb_id):
        """Add movie to CouchPotato wanted list by IMDB ID"""
        return self.make_request('movie.add', {
            'identifier': imdb_id,
        })

def search(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.search(args.query)
    movies = [Movie(**m) for m in data['movies']]
    fields = [
        'title',
        'year',
        'imdb',
    ]
    rows = []
    for movie in movies:
        row = []
        for field in fields:
            val = None
            try:
                row.append(getattr(movie, field))
            except:
                row.append('-')
        rows.append(row)
    print(tabulate(rows, headers=fields))

def add(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.add(args.id)
    print(data)

def main():
    args = parse_args()
    args.function(args)


if __name__ == '__main__':
    main()

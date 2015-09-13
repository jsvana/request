import argparse
import http.client
import json
from tabulate import tabulate
import urllib.parse
import ssl
import time

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

    list_parser = subparsers.add_parser(
        'list',
        parents=[type_args],
        help='list all media',
    )
    list_parser.set_defaults(function=list_media)

    view_queued_parser = subparsers.add_parser(
        'view-queued',
        parents=[type_args],
        help='view all queued media objects',
    )
    view_queued_parser.set_defaults(function=view_queued)

    notifications_parser = subparsers.add_parser(
        'notifications',
        parents=[type_args],
        help='view all notifications',
    )
    notifications_parser.set_defaults(function=notifications)

    command_parser = subparsers.add_parser(
        'command',
        parents=[type_args],
        help='run api command',
    )
    command_parser.add_argument(
        'cmd',
        help='command to run',
    )
    command_parser.set_defaults(function=command)

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

    def get_all(self):
        return self.make_request('movie.list')

    def add(self, imdb_id):
        """Add movie to CouchPotato wanted list by IMDB ID"""
        return self.make_request('movie.add', {
            'identifier': imdb_id,
        })

    def get_queued(self):
        """Get all queued movies"""
        return self.make_request('movie.list', {
            'status': 'active',
        })

    def command(self, cmd):
        """Run arbitrary command"""
        return self.make_request(cmd)

def search(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.search(args.query)
    movies = [Movie(**m) for m in data['movies']]
    fields = [
        'title',
        'year',
        'imdb',
        'status',
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
    #print(data)

def _print_movies(movies, fields=None):
    movies = [Movie(**m) for m in movies]
    if fields is None:
        fields = [
            'title',
            'year',
            'imdb',
            'status',
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

def list_media(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.get_all()
    _print_movies(data['movies'])

def view_queued(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.get_queued()
    _print_movies(data['movies'], fields=[
        'title',
        'year',
        'imdb',
    ])

def notifications(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.command('notification.list')
    unread = []
    for notif in data['notifications']:
        if 'read' not in notif or not notif['read']:
            unread.append(notif)
    rows = []
    for notif in unread:
        rows.append([
            notif['message'],
            time.ctime(notif['time']),
        ])
    print(tabulate(reversed(rows), headers=[
        'message',
        'time'
    ]))

def command(args):
    api = CouchpotatoApi(config.couchpotato_key)
    data = api.command(args.cmd)
    print(json.dumps(data, indent=4))

def list_functions(args):
    print('Enabled APIs:')
    print('CouchPotato')
    print()
    print('See main.py --help for more information')

def main():
    args = parse_args()
    #try:
    args.function(args)
    #except:
        #list_functions(args)

if __name__ == '__main__':
    main()

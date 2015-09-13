import http.client
import json
from tabulate import tabulate
import urllib.parse
import ssl
import time

from ..config import couchpotato_key
from ..media import Movie
from base import Consumer

class CouchPotato(Consumer):
    def __init__(self):
        super().__init__(couchpotato_key)
        self.app_base_route = '/couchpotato/api'

    @classmethod
    def add_commands(cls, subparsers):
        parser = subparsers.add_parser(
            'couchpotato',
            help='various commands for couchpotato',
        )
        potato_parsers = parser.add_subparsers()
        search_parser = potato_parsers.add_parser(
            'search',
            help='search for a given movie',
        )
        search_parser.add_argument(
            'query',
            help='query term to search for',
        )
        search_parser.set_defaults(cls=cls, function='search')

        add_parser = potato_parser.add_parser(
            'add',
            help='add a given media object by id',
        )
        add_parser.add_argument(
            'id',
            help='ID of media to add',
        )
        add_parser.set_defaults(cls=cls, function='add')

        list_parser = potato_parser.add_parser(
            'list',
            parents=[type_args],
            help='list all media',
        )
        list_parser.set_defaults(cls=cls, function='list_media')

        view_queued_parser = potato_parser.add_parser(
            'view-queued',
            parents=[type_args],
            help='view all queued media objects',
        )
        view_queued_parser.set_defaults(cls=cls, function='view_queued')

        notifications_parser = potato_parser.add_parser(
            'notifications',
            parents=[type_args],
            help='view all notifications',
        )
        notifications_parser.set_defaults(cls=cls, function='notifications')

    def _print_movies(self, movies, fields=None):
        if fields is None:
            fields = [
                'title',
                'year',
                'imdb',
            ]
        self.print_objects(movies, fields, cls=Movie)

    def search(self, args):
        """Search for given movie title"""
        data = self.make_request('search', {
            'q': args.query,
        })
        self._print_movies(data['movies'])

    def get_all(self, args):
        """Get a list of all movies on the server"""
        data = self.make_request('movie.list')
        self._print_movies(data['movies'])

    def add(self, args):
        """Add movie to wanted list by IMDB ID"""
        self.make_request('movie.add', {
            'identifier': args.id,
        })
        print('Sent add request to server')

    def get_queued(self, args):
        """Get all queued movies"""
        data = self.make_request('movie.list', {
            'status': 'active',
        })
        self._print_movies(data['movies'], fields=[
            'title',
            'year',
            'imdb',
        ])

    def notifications(self, args):
        data = self.make_request('notification.list')
        unread = []
        for notif in data['notifications']:
            if 'read' not in notif or not notif['read']:
                unread.append(notif)
        self.print_objects(unread, ['message', 'time'])

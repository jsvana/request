import time

from ..config import couchpotato_key
from ..media import Movie
from .base import Consumer

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

        potato_parser = parser.add_subparsers()
        search_parser = potato_parser.add_parser(
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
            help='add a movie',
        )
        group = add_parser.add_mutually_exclusive_group()
        group.add_argument(
            '--id',
            metavar='IMDB_ID',
            help='IMDB ID of movie to add',
        )
        group.add_argument(
            '--title',
            metavar='MOVIE_TITLE',
            help='title of movie to add. Must be a title returned by the '
            '`search` command',
        )
        add_parser.set_defaults(cls=cls, function='add')

        list_parser = potato_parser.add_parser(
            'list',
            help='list all movies',
        )
        list_parser.set_defaults(cls=cls, function='get_all')

        view_queued_parser = potato_parser.add_parser(
            'queued',
            help='view all queued movies',
        )
        view_queued_parser.set_defaults(cls=cls, function='get_queued')

        notifications_parser = potato_parser.add_parser(
            'notifications',
            help='view all notifications',
        )
        notifications_parser.set_defaults(cls=cls, function='notifications')

    def _print_movies(self, movies, fields=None):
        """Helper wrapper around print_objects"""
        if fields is None:
            fields = [
                'title',
                'year',
                'imdb',
            ]
        self.print_objects(movies, fields, cls=Movie)

    def help(self, args):
        """Help for base couchpotato command"""
        print('Various commands for couchpotato')
        print('run with --help for more information')

    def search(self, args):
        """Search for given movie title"""
        data = self.make_request('search', {
            'q': args.query,
        })
        self._print_movies(data['movies'])

    def get_all(self, args):
        """Get a list of all movies on the server"""
        data = self.make_request('movie.list')
        self._print_movies(data['movies'], [
            'title',
            'status',
            'type',
        ])

    def add(self, args):
        """Add movie to wanted list by IMDB ID or title"""
        query = {}
        if args.id is not None:
            query['identifier'] = args.id
        elif args.title is not None:
            query['title'] = args.title
        self.make_request('movie.add', query)
        print('Sent add request to server')

    def get_queued(self, args):
        """Get all queued movies"""
        data = self.make_request('movie.list', {
            'status': 'active',
        })
        self._print_movies(data['movies'], fields=[
            'title',
            'type',
        ])

    def notifications(self, args):
        data = self.make_request('notification.list')
        unread = []
        for notif in data['notifications']:
            if 'read' not in notif or not notif['read']:
                unread.append(notif)
        self.print_objects(unread, {
            'message': None,
            'time': lambda t: time.ctime(int(t)),
        }, reverse=True)

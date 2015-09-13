import json
import time

from ..config import sickbeard_key
from ..media import Show
from .base import Consumer

class Sickbeard(Consumer):
    def __init__(self):
        super().__init__(sickbeard_key)
        self.app_base_route = '/sickbeard/api'

    @classmethod
    def add_commands(cls, subparsers):
        parser = subparsers.add_parser(
            'sickbeard',
            help='various commands for sickbeard',
        )

        beard_parser = parser.add_subparsers()
        # search_parser = beard_parser.add_parser(
            # 'search',
            # help='search for a given movie',
        # )
        # search_parser.add_argument(
            # 'query',
            # help='query term to search for',
        # )
        # search_parser.set_defaults(cls=cls, function='search')

        # add_parser = beard_parser.add_parser(
            # 'add',
            # help='add a movie',
        # )
        # group = add_parser.add_mutually_exclusive_group()
        # group.add_argument(
            # '--id',
            # metavar='IMDB_ID',
            # help='IMDB ID of movie to add',
        # )
        # group.add_argument(
            # '--title',
            # metavar='MOVIE_TITLE',
            # help='title of movie to add. Must be a title returned by the '
            # '`search` command',
        # )
        # add_parser.set_defaults(cls=cls, function='add')

        list_parser = beard_parser.add_parser(
            'list',
            help='list all shows',
        )
        list_parser.set_defaults(cls=cls, function='get_all')

        logs_parser = beard_parser.add_parser(
            'logs',
            help='get most recent sickbeard logs',
        )
        logs_parser.set_defaults(cls=cls, function='logs')

        # view_queued_parser = beard_parser.add_parser(
            # 'queued',
            # help='view all queued movies',
        # )
        # view_queued_parser.set_defaults(cls=cls, function='get_queued')

        notifications_parser = beard_parser.add_parser(
            'notifications',
            help='view all notifications',
        )
        notifications_parser.set_defaults(cls=cls, function='notifications')

    def _print_shows(self, shows, fields=None):
        """Helper wrapper around print_objects"""
        if fields is None:
            fields = [
                'show_name',
                'status',
                'network',
                'quality',
            ]
        shows = shows['data'].values()
        self.print_objects(shows, fields, cls=Show)

    def help(self, args):
        """Help for base sickbeard command"""
        print('Various commands for sickbeard')
        print('run with --help for more information')

    def get_all(self, args):
        """Get a list of all movies on the server"""
        data = self.make_request('shows')
        self._print_shows(data)

    def logs(self, args):
        """Show most recent sickbeard logs"""
        logs = self.make_request('logs')
        print('\n'.join(logs['data']))

    def notifications(self, args):
        data = self.make_request('sb.getmessages')
        self.print_objects(data['data'], [
            'title',
            'message',
            'type',
        ])

import json
import time

from ..config import headphones_key
from ..media import Show
from .base import Consumer

class Headphones(Consumer):
    def __init__(self):
        super().__init__(headphones_key)
        self.app_base_route = '/headphones/api'

    @classmethod
    def add_commands(cls, subparsers):
        parser = subparsers.add_parser(
            'headphones',
            help='various commands for headphones',
        )

        phones_parser = parser.add_subparsers()

        list_parser = phones_parser.add_parser(
            'list',
            help='list all shows',
        )
        list_parser.set_defaults(cls=cls, function='get_all')

        logs_parser = phones_parser.add_parser(
            'logs',
            help='get most recent headphones logs',
        )
        logs_parser.set_defaults(cls=cls, function='logs')

        # view_queued_parser = phones_parser.add_parser(
            # 'queued',
            # help='view all queued movies',
        # )
        # view_queued_parser.set_defaults(cls=cls, function='get_queued')

        history_parser = phones_parser.add_parser(
            'history',
            help='view history',
        )
        history_parser.set_defaults(cls=cls, function='history')

    def _print_shows(self, shows, fields=None):
        """Helper wrapper around print_objects"""
        if fields is None:
            fields = [
                'ArtistName',
            ]
        shows = shows['data'].values()
        self.print_objects(shows, fields, cls=Show)

    def help(self, args):
        """Help for base headphones command"""
        print('Various commands for headphones')
        print('run with --help for more information')

    def get_all(self, args):
        """Get a list of all movies on the server"""
        data = self.make_request('&cmd=getIndex')
        self._print_shows(data)

    def history(self, args):
        data = self.make_request('&cmd=getHistory')
        data = json.load(data)
        print(data['Title', 'Size'])
        self.print_objects(data[
            'Status',
            'DateAdded',
            'Title',
            'URL',
            'FolderName',
            'AlbumID',
            'Size',
        ])

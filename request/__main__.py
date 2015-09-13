import argparse
import http.client
import json
from tabulate import tabulate
import urllib.parse
import ssl
import time

from . import config
from .consumers.couchpotato import CouchPotato
from .media import Movie

SUPPORTED_CONSUMERS = [
    CouchPotato,
]

def parse_args():
    parser = argparse.ArgumentParser()
    # TODO(jsvana): move to logger
    # parser.add_argument(
        # '-v', '--verbose',
        # action='store_true',
        # help='print more output',
    # )
    subparsers = parser.add_subparsers()

    for consumer in SUPPORTED_CONSUMERS:
        consumer.add_commands(subparsers)

    return parser.parse_args()

def list_functions(args):
    print('Enabled consumers:')
    for cls in SUPPORTED_CONSUMERS:
        print(cls.__name__)
    print()
    print('See main.py --help for more information')

def main():
    args = parse_args()
    if hasattr(args, 'cls'):
        obj = args.cls()
        if hasattr(args, 'function'):
            func = getattr(obj, args.function)
        else:
            func = getattr(obj, 'help')
        func(args)

    else:
        list_functions(args)

if __name__ == '__main__':
    main()

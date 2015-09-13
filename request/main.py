import argparse
import http.client
import json
from tabulate import tabulate
import urllib.parse
import ssl
import time

import config
from consumers.couchpotato import CouchPotato
from media import Movie

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
    [print(cls.__name__) for cls in SUPPORTED_CONSUMERS]
    print()
    print('See main.py --help for more information')

def main():
    args = parse_args()
    obj = args.cls()
    func = getattr(obj, args.function)
    func(obj, args)

if __name__ == '__main__':
    main()

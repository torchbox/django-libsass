#!/usr/bin/env python

import argparse
import os
import shutil
import sys
import warnings

from django.core.management import execute_from_command_line

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deprecation', choices=['pending', 'imminent', 'none'], default='imminent')
    return parser


def parse_args(args=None):
    return make_parser().parse_known_args(args)


def runtests():
    args, rest = parse_args()

    if args.deprecation == 'pending':
        # Show all deprecation warnings
        warnings.simplefilter('default', DeprecationWarning)
        warnings.simplefilter('default', PendingDeprecationWarning)
    elif args.deprecation == 'imminent':
        # Show only imminent deprecation warnings
        warnings.simplefilter('default', DeprecationWarning)
    elif args.deprecation == 'none':
        # Deprecation warnings are ignored by default
        pass

    argv = [sys.argv[0], 'test'] + rest

    try:
        execute_from_command_line(argv)
    finally:
        from tests.settings import STATIC_ROOT
        shutil.rmtree(STATIC_ROOT, ignore_errors=True)


if __name__ == '__main__':
    runtests()

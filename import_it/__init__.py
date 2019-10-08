#!/usr/bin/env python3.7
import os
import argparse
import logging
import re
from ripgrepy import Ripgrepy

from .utils import trim_prefix, trim_suffix


loglevel = os.getenv('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=getattr(logging, loglevel))

logger = logging.getLogger(__file__)


def try_to_match_on_existing_import(symbol, repository):
    search = rf'import \b{symbol}\b'
    result = Ripgrepy(search, repository).json().run().as_dict
    import_source = result[0]['data']['lines']['text'].rstrip()
    return import_source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')
    parser.add_argument('repository')
    parser.add_argument('filepath', nargs='?', default='')
    args = parser.parse_args()

    symbol = args.symbol
    repository = args.repository
    filepath = args.filepath

    if re.fullmatch('[A-Z_]+', symbol):
        search = rf'^{symbol}\s=\s'
    elif symbol[0].isupper():
        search = rf'class {symbol}\('
    else:
        search = rf'def {symbol}\b'

    logger.info(f'Running ripgrep with search {search}')
    result = Ripgrepy(search, repository).json().run().as_dict

    if not result:
        logger.info('Trying to match on existing import')
        import_source = try_to_match_on_existing_import(symbol, repository)
    else:
        absolute_path = result[0]['data']['path']['text']

        filepath_parts = filepath.split('/')
        absolute_path_parts = absolute_path.split('/')

        if filepath_parts[:-1] == absolute_path_parts[:-1]:
            logger.info('Will do relative path')

            relative_path = f'.{absolute_path_parts[-1]}'
        else:
            relative_path = trim_prefix(absolute_path, f'{repository}/')

        filename_no_extension = trim_suffix(relative_path, '.py')

        import_path = trim_suffix(filename_no_extension, '/__init__').replace('/', '.')

        import_source = f'from {import_path} import {symbol}'

    print(import_source)


if __name__ == '__main__':
    main()

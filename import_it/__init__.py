#!/usr/bin/env python3.7
import argparse
import re
from ripgrepy import Ripgrepy


def trim_prefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def try_to_match_on_existing_import(symbol, repository):
    search = rf'import \b{symbol}\b'
    result = Ripgrepy(search, repository).json().run().as_dict
    import_source = result[0]['data']['lines']['text'].rstrip()
    return import_source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')
    parser.add_argument('repository')
    args = parser.parse_args()

    symbol = args.symbol
    repository = args.repository

    if re.fullmatch('[A-Z_]+', symbol):
        search = rf'{symbol}\s=\s'
    elif symbol[0].isupper():
        search = f'class {symbol}'
    else:
        search = f'def {symbol}'

    result = Ripgrepy(search, repository).json().run().as_dict

    if not result:
        import_source = try_to_match_on_existing_import(symbol, repository)
    else:
        absolute_path = result[0]['data']['path']['text']

        relative_path = trim_prefix(absolute_path, repository)

        import_path = (
            trim_prefix(relative_path, '/').replace('.py', '').replace('/', '.')
        )

        import_source = f'from {import_path} import {symbol}'

    print(import_source)


if __name__ == '__main__':
    main()

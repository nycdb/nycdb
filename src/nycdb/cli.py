import argparse
import logging
from .dataset import Dataset


def parse_args():
    parser = argparse.ArgumentParser(description='NYC-DB: utilities for the database of NYC housing data')
    parser.add_argument('--download', action='store', help='downloads file for provided dataset')
    parser.add_argument("-U", "--user", help="Postgres user. default: postgres", default="postgres")
    parser.add_argument("-P", "--password", help="Postgres password. default: postgres", default="postgres")
    parser.add_argument("-H", "--host", help="Postgres host: default: 127.0.0.1", default="127.0.0.1")
    parser.add_argument("-D", "--database", help="postgres database: default: postgres", default="postgres")
    return parser.parse_args()


def dispatch(args):
    if args.download:
        Dataset(args.download).download_files()


def main():
    args = parse_args()
    dispatch(args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

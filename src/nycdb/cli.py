import argparse
import logging
from .dataset import Dataset, datasets


def parse_args():
    parser = argparse.ArgumentParser(description='NYC-DB: utilities for the database of NYC housing data')

    # Download, Load, Verify a dataset
    parser.add_argument('--download', action='store', help='downloads file for provided dataset')
    parser.add_argument('--load', action='store', help='loads dataset into postgres')
    parser.add_argument('--verify', action='store', help='verifies a dataset by checking the table row count')
    # list and verify
    parser.add_argument('--list-datasets', action='store_true', help='lists all datasets')
    parser.add_argument('--verify-all', action='store_true', help='verifies all datasets')
    # DB CONNECTION
    parser.add_argument("-U", "--user", help="Postgres user. default: postgres", default="postgres")
    parser.add_argument("-P", "--password", help="Postgres password. default: postgres", default="postgres")
    parser.add_argument("-H", "--host", help="Postgres host: default: 127.0.0.1", default="127.0.0.1")
    parser.add_argument("-D", "--database", help="postgres database: default: postgres", default="postgres")
    parser.add_argument("--port", help="Postgres port: default: 5432", default="5432")
    # change location of data dir
    parser.add_argument("--root-dir", help="location of data directory", default="./data")
    return parser.parse_args()


def print_datasets():
    for ds in datasets().keys():
        print(ds)


def verify_all(args):
    for ds in datasets().keys():
        Dataset(ds, args=args).verify()


def dispatch(args):
    if args.list_datasets:
        print_datasets()
    elif args.verify:
        Dataset(args.verify, args=args).verify()
    elif args.verify_all:
        verify_all(args)
    elif args.download:
        Dataset(args.download, args=args).download_files()
    elif args.load:
        Dataset(args.load, args=args).db_import()


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    dispatch(args)


if __name__ == '__main__':
    main()

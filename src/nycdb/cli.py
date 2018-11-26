import argparse
import logging
import os
import subprocess
import sys
from .dataset import Dataset, datasets


POSTGRES_USER = os.environ.get('NYCDB_POSTGRES_USER', 'nycdb')
POSTGRES_PASSWORD = os.environ.get('NYCDB_POSTGRES_PASSWORD', 'nycdb')
POSTGRES_HOST = os.environ.get('NYCDB_POSTGRES_HOST', '127.0.0.1')
POSTGRES_DB = os.environ.get('NYCDB_POSTGRES_DB', 'nycdb')
POSTGRES_PORT = os.environ.get('NYCDB_POSTGRES_PORT', '5432')


def parse_args():
    parser = argparse.ArgumentParser(description='NYC-DB: utilities for the database of NYC housing data')

    # Download, Load, Verify, Dump
    parser.add_argument('--download', action='store', help='downloads file for provided dataset')
    parser.add_argument('--load', action='store', help='loads dataset into postgres')
    parser.add_argument('--verify', action='store', help='verifies a dataset by checking the table row count')
    parser.add_argument('--dump', action='store', help='creates a sql dump of the datasets in the current folder')
    # list and verify
    parser.add_argument('--list-datasets', action='store_true', help='lists all datasets')
    parser.add_argument('--verify-all', action='store_true', help='verifies all datasets')
    # DB CONNECTION
    parser.add_argument(
        "-U",
        "--user",
        help="Postgres user. default: {}".format(POSTGRES_USER),
        default=POSTGRES_USER
    )
    parser.add_argument(
        "-P",
        "--password",
        help="Postgres password. default: {}".format(POSTGRES_PASSWORD),
        default=POSTGRES_PASSWORD
    )
    parser.add_argument(
        "-H",
        "--host",
        help="Postgres host: default: {}".format(POSTGRES_HOST),
        default=POSTGRES_HOST
    )
    parser.add_argument(
        "-D",
        "--database",
        help="postgres database: default: {}".format(POSTGRES_DB),
        default=POSTGRES_DB
    )
    parser.add_argument(
        "--port",
        help="Postgres port: default: {}".format(POSTGRES_PORT),
        default=POSTGRES_PORT
    )
    # change location of data dir
    parser.add_argument("--root-dir", help="location of data directory", default="./data")
    # easily inspect the database from the command-line
    parser.add_argument("--dbshell", action="store_true", help="runs psql interactively")
    return parser.parse_args()


def print_datasets():
    for ds in datasets().keys():
        print(ds)


def verify_all(args):
    for ds in datasets().keys():
        Dataset(ds, args=args).verify()


def run_dbshell(args):
    env = os.environ.copy()
    env['PGPASSWORD'] = args.password
    retval = subprocess.call([
        'psql', '-h', args.host, '-p', args.port, '-U', args.user, '-d', args.database
    ], env=env)
    sys.exit(retval)


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
    elif args.dump:
        Dataset(args.dump, args=args).dump()
    elif args.dbshell:
        run_dbshell(args=args)

def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    dispatch(args)


if __name__ == '__main__':
    main()

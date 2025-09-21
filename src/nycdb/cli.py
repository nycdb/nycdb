import argparse
import logging
import sys
from .dataset import Dataset
from .datasets import datasets


def parse_args():
    parser = argparse.ArgumentParser(description='NYCDB: database utilities for NYC housing data')

    # Download, Load, Verify, Dump
    parser.add_argument('--download', metavar='DATASET', action='store', help='downloads file for provided dataset')
    parser.add_argument('--load', metavar='DATASET', action='store', help='loads dataset into postgres')
    parser.add_argument('--verify', metavar='DATASET', action='store', help='verifies a dataset by checking the table row count')
    parser.add_argument('--dump', metavar='DATASET', action='store', help='creates a sql dump of the datasets in the current folder')
    parser.add_argument('--drop', metavar='DATASET', action='store', help='deletes a dataset from postgres')
    # list and verify
    parser.add_argument('--list-datasets', action='store_true', help='lists all datasets')
    parser.add_argument('--verify-all', action='store_true', help='verifies all datasets')
    # DB CONNECTION
    parser.add_argument("--db-path", help="location of duckdb file", default="nycdb.duckdb")
    # change location of data dir
    parser.add_argument("--root-dir", help="location of data directory", default="./data")

    parser.add_argument("--hide-progress", action="store_true", help="hide the progress bar")
    return parser.parse_args()


def print_datasets():
    for ds in sorted(datasets().keys()):
        print(ds)


def verify_all(args):
    exit_status = 0

    for ds in sorted(datasets().keys()):
        if not Dataset(ds, args=args).verify():
            exit_status = 1

    sys.exit(exit_status)


def dispatch(args):
    if args.list_datasets:
        print_datasets()
    elif args.verify:
         if Dataset(args.verify, args=args).verify():
             sys.exit(0)
         else:
             sys.exit(1)
    elif args.verify_all:
        verify_all(args)
    elif args.download:
        Dataset(args.download, args=args).download_files()
    elif args.load:
        Dataset(args.load, args=args).db_import()
    elif args.dump:
        Dataset(args.dump, args=args).dump()
    elif args.drop:
        Dataset(args.drop, args=args).drop()

def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    dispatch(args)


if __name__ == '__main__':
    main()

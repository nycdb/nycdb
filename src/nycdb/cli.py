import argparse
import logging
from .dataset import Dataset


def parse_args():
    parser = argparse.ArgumentParser(description='NYC-DB: utilities for the database of NYC housing data')
    parser.add_argument('--download', action='store', help='downloads file for provided dataset')
    return parser.parse_args()


def dispatch(args):
    if args.download:
        Dataset(args.download).download_files()


def main():
    args = parse_args()
    dispatch(args)


if __name__ == '__main__':
    main()

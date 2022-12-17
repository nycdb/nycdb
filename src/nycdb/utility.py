import os
from pathlib import Path
from itertools import islice
import yaml


def read_yml(file):
    """Reads a yaml file and outputs a Dictionary"""
    with open(file, 'r') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


def mkdir(file_path):
    """ Creates all parent directories"""
    Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)


def list_wrap(x):
    """
    Returns input if is an tuple or list,
    otherwise it wraps x in an list
    """
    if isinstance(x, list) or isinstance(x, tuple):
        return x
    else:
        return [x]


def merge(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def consume(iterator, n):
    """advance the iterator n-steps ahead"""
    next(islice(iterator, n, n), None)

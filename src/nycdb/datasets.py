import os

from functools import lru_cache
from pathlib import Path
from .utility import read_yml
from . import plugins


def iter_dataset_yaml_files():
    for plugin in plugins.iter_plugins():
        yield from plugin.root_dir.glob('./datasets/*.yml')


@lru_cache()
def datasets():
    """
    Returns a dictionary with all defined datasets.
    """
    dataset_dictionary = {}

    for yaml_file in iter_dataset_yaml_files():
        dataset_dictionary[yaml_file.stem] = read_yml(yaml_file)

    return dataset_dictionary

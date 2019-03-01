import os

from functools import lru_cache
from pathlib import Path
from .utility import read_yml

@lru_cache()
def datasets():
    """
    Returns a dictionary with all defined datasets.
    """
    dataset_dictionary = {}

    for yaml_file in Path(os.path.dirname(__file__)).absolute().glob('./datasets/*.yml'):
        dataset_dictionary[yaml_file.stem] = read_yml(yaml_file)

    return dataset_dictionary

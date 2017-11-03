import logging
import os
import requests
import yaml
from pathlib import Path
from functools import lru_cache

def read_yml(file):
    """Reads a yaml file and outputs a Dictionary"""
    with open(file, 'r') as yaml_file:
        return yaml.load(yaml_file)

    
@lru_cache()
def datasets():
    """Returns a dictionary with all defined datasets"""
    return read_yml(os.path.join(os.path.dirname(__file__), 'datasets.yml'))


class DownloadFailedException(Exception):
    pass


def mkdir(file_path):
    """ Creates directories for the file path"""
    Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

    
def download_file(url, dest):
    mkdir(dest)
    try:
        r = requests.get(url, stream=True)
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=(512 * 1024)): 
                if chunk: 
                    f.write(chunk)
        return True
    except:
        raise DownloadFailedException("Could not download: {}".format(url))

    
class File:
    """Wrapper around a file"""

    def __init__(self, file_dict, root_dir='./data', folder=''):
        self.root_dir = root_dir
        self.url = file_dict['url']
        self.dest = self._dest(file_dict)


    def download(self):
        download_file(self.url, self.dest)
        return self

    def _dest(self, file_dict):
        if 'dest' in file_dict:
            file_path = file_dict['dest']
        else:
            file_path = file_dict['url'].split('/')[-1]
        return os.path.abspath(os.path.join(self.root_dir, file_path))


class Dataset:
    """Information about a dataset"""

    def __init__(self, dataset_name):
        self.name = dataset_name
        self.dataset = datasets()[dataset_name]
        self.files = self._files()

    def _files(self):
        return [ File(file_dict, folder=self.name) for file_dict in self.dataset['files'] ]


    def download_files(self):
        for f in self.files:
            f.download()


class Datasets:
    """ All NYCDB datasets """
    
    def __init__(self):
        self.datasets = [ Dataset(k) for k in datasets() ]


    def download_all(self):
        for d in self.datasets:
            d.download_Files()

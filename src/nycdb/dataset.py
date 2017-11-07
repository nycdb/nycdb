import logging
import os
import requests
import yaml
from pathlib import Path
from functools import lru_cache
from . import dataset_transformations
from . import sql
from .database import Database
from .typecast import Typecast

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
    """ 
    Downloads a url and saves the result to the destination path
    
    It will creates parent directory of the destination path,
    if they they don't exist.
    

    If the destination file exists and is not empty, it assumes the file has
    already been downloaded and will skip downloading the file accordingly.
    """
    mkdir(dest)

    if Path(dest).exists() and os.stat(dest).st_size > 0:
        logging.info("{} has already been downloaded, skipping".format(url))
        return True

    try:
        logging.info("Downloading {url} to {dest}".format(url=url, dest=dest))
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

    def __init__(self, dataset_name, args=None):
        self.name = dataset_name
        self.args = args
        self.db = Database(self.args, table_name=self.name)
        self.dataset = datasets()[dataset_name]
        self.typecast = Typecast(self)
        self.files = self._files()
        # self.import_file = None

    def _files(self):
        return [ File(file_dict, folder=self.name, root_dir=self.args.root_dir) for file_dict in self.dataset['files'] ]


    def download_files(self):
        for f in self.files:
            f.download()


    def transform(self):
        """ 
        Calls the function in dataset_transformation with the same name
        as the dataset
        """
        return self.typecast.cast_rows(getattr(dataset_transformations, self.name)(self))
        

    def db_import(self):
        self.create_table()
        for row in self.transform():
            self.db.insert(row)

    def create_table(self):
        self.db.sql(sql.create_table(self.name, self.dataset['schema']['fields']))
    

class Datasets:
    """ All NYCDB datasets """
    
    def __init__(self, args):
        self.args = args
        self.datasets = [ Dataset(k, args=args) for k in datasets() ]

    def download_all(self):
        for d in self.datasets:
            d.download_files()


    def transform_all(self):
        for d in self.datasets:
            d.transfrom_files()
            

    def import_all(self):
        for d in self.datasets:
            d.db_import()

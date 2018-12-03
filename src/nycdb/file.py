import codecs
import os
import requests
import logging
from pathlib import Path
from tqdm import tqdm
from .utility import mkdir


class DownloadFailedException(Exception):
    pass


open_str_kwargs = {'mode': 'w', 'encoding': 'utf-8', 'errors': 'replace'}
open_byte_kwargs = {'mode': 'wb'}


def is_csv(dest):
    return dest[-4:].lower() == '.csv'


def open_kwargs(dest):
    if is_csv(dest):
        return open_str_kwargs
    else:
        return open_byte_kwargs


def safe_int(value):
    """
    Attempt to convert the given value to an integer,
    returning None on failure.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


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
        is_csv_file = is_csv(dest)
        r = requests.get(url, stream=True)
        total_bytes = safe_int(r.headers.get('content-length'))
        pbar = tqdm(total=total_bytes, unit='B', unit_scale=True, unit_divisor=1024)
        with open(dest, **open_kwargs(dest)) as f:
            for chunk in r.iter_content(chunk_size=(512 * 1024)):
                if chunk:
                    pbar.update(len(chunk))
                    if is_csv_file:
                        f.write(codecs.decode(chunk, encoding='utf-8', errors='replace'))
                    else:
                        f.write(chunk)
        pbar.close()
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

import codecs
import os
import re
import requests
import logging
from pathlib import Path
from urllib.parse import urlsplit
from tqdm import tqdm
from .utility import mkdir


class DownloadFailedException(Exception):
    pass


# SODA3 query endpoints require an app token (or user authentication).
# The token is read from this environment variable and is sent, as the
# X-App-Token header, only to query.csv URLs on these Socrata hosts.
SOCRATA_APP_TOKEN_ENV = 'NYCDB_SOCRATA_APP_TOKEN'
SOCRATA_HOSTS = frozenset(['data.cityofnewyork.us', 'data.ny.gov'])
SOCRATA_QUERY_PATH = re.compile(r'^/api/v3/views/[a-z0-9]{4}-[a-z0-9]{4}/query\.csv$')
VALID_APP_TOKEN = re.compile(r'^[\x21-\x7e]+$')

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


def is_socrata_query(url):
    """
    True if url is a SODA3 query.csv endpoint on an approved Socrata host,
    over https on the default port.
    """
    try:
        parts = urlsplit(url)
        return (parts.scheme == 'https'
                and parts.hostname in SOCRATA_HOSTS
                and parts.port is None
                and parts.username is None
                and SOCRATA_QUERY_PATH.match(parts.path) is not None)
    except ValueError:
        return False


def socrata_app_token():
    """
    Returns the app token from NYCDB_SOCRATA_APP_TOKEN, or None if it is
    not set. The token value is never included in an error message.
    """
    token = os.environ.get(SOCRATA_APP_TOKEN_ENV, '').strip()
    if not token:
        return None
    if not VALID_APP_TOKEN.match(token):
        raise DownloadFailedException(
            "{} contains characters that are not allowed in an HTTP header".format(SOCRATA_APP_TOKEN_ENV))
    return token


def download_file(url, dest, hide_progress=False):
    """
    Downloads a url and saves the result to the destination path

    It will creates parent directory of the destination path,
    if they they don't exist.

    If the destination file exists and is not empty, it assumes the file has
    already been downloaded and will skip downloading the file accordingly.

    Socrata SODA3 query.csv URLs are sent the app token from
    NYCDB_SOCRATA_APP_TOKEN, if set. Those requests do not follow redirects,
    so the token is never sent to another URL.

    A response with an HTTP error status, or a download that fails part way,
    raises DownloadFailedException and leaves no file at the destination.
    """
    mkdir(dest)

    if Path(dest).exists() and os.stat(dest).st_size > 0:
        logging.info("{} has already been downloaded, skipping".format(url))
        return True

    headers = {}
    socrata_query = is_socrata_query(url)
    if socrata_query:
        token = socrata_app_token()
        if token:
            headers['X-App-Token'] = token
        else:
            logging.warning("{} is not set. Socrata requires an app token for {}".format(SOCRATA_APP_TOKEN_ENV, url))

    try:
        logging.info("Downloading {url} to {dest}".format(url=url, dest=dest))
        is_csv_file = is_csv(dest)
        if socrata_query:
            r = requests.get(url, stream=True, headers=headers, allow_redirects=False)
        else:
            r = requests.get(url, stream=True)
        check_response(r, url, socrata_query and not headers)
        total_bytes = safe_int(r.headers.get('content-length'))
        pbar = tqdm(total=total_bytes, unit='B', unit_scale=True, unit_divisor=1024, disable=hide_progress)
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
    except (requests.RequestException, OSError) as e:
        remove_partial(dest)
        raise DownloadFailedException("Could not download {}: {}".format(url, e))
    except DownloadFailedException:
        remove_partial(dest)
        raise


def check_response(r, url, missing_socrata_token=False):
    """
    Raises DownloadFailedException unless the response is a 2xx success.
    """
    if 200 <= r.status_code < 300:
        return
    r.close()
    message = "Could not download {}: HTTP {}".format(url, r.status_code)
    if r.status_code in (401, 403) and missing_socrata_token:
        message += ". Set {} to a Socrata app token".format(SOCRATA_APP_TOKEN_ENV)
    elif 300 <= r.status_code < 400:
        message += " redirect was not followed"
    raise DownloadFailedException(message)


def remove_partial(dest):
    try:
        os.remove(dest)
    except FileNotFoundError:
        pass


class File:
    """Wrapper around a file"""

    def __init__(self, file_dict, root_dir='./data', folder=''):
        self.root_dir = root_dir
        self.url = file_dict['url']
        self.dest = self._dest(file_dict)

    def download(self, hide_progress=False):
        download_file(self.url, self.dest, hide_progress=hide_progress)
        return self

    def _dest(self, file_dict):
        if 'dest' in file_dict:
            file_path = file_dict['dest']
        else:
            file_path = file_dict['url'].split('/')[-1]
        return os.path.abspath(os.path.join(self.root_dir, file_path))

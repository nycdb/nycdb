import nycdb
import os
import time
import http.server
import psycopg2
from multiprocessing import Process
from unittest.mock import patch
from types import SimpleNamespace

ARGS = SimpleNamespace(user='postgres', password='password', host='127.0.0.1', database='postgres', port='7777', root_dir='./data')

def test_datasets():
    assert type(nycdb.datasets()) is dict
    assert type(nycdb.datasets()['pluto_16v2']) is dict


def test_dataset():
    d = nycdb.Dataset('pluto_16v2', args=ARGS)

    assert d.name == 'pluto_16v2'
    assert d.dataset == nycdb.datasets()['pluto_16v2']
    assert isinstance(d.files, list)
    assert len(d.files) == 1
    assert isinstance(d.files[0], nycdb.File)


@patch('psycopg2.connect')
def test_setup_db(mock_connect):
    d = nycdb.Dataset('pluto_16v2', args=ARGS)
    assert d.db is None
    d.setup_db()
    d.setup_db()
    assert isinstance(d.db, nycdb.Database)
    assert mock_connect.call_count == 1
    

def test_file_constructor_with_dest():
    file_dict = { 'url': 'http://example.com', 'dest': 'example.csv' }
    f = nycdb.File(file_dict)
    assert f.url == 'http://example.com'
    assert f.dest == os.path.abspath('./data/example.csv')


def test_file_constructor_without_dest():
    file_dict = { 'url': 'http://example.com/test.csv' }
    f = nycdb.File(file_dict)
    assert f.dest == os.path.abspath('./data/test.csv')


def test_mkdir(tmpdir):
    file_path = tmpdir.join('directory/file.zip')
    assert tmpdir.join('directory').check() is False
    assert file_path.check() is False
    nycdb.dataset.mkdir(file_path.strpath)
    assert tmpdir.join('directory').check() is True
    assert file_path.check() is False
    # check that it can be run again without errors:
    nycdb.dataset.mkdir(file_path.strpath)
    assert tmpdir.join('directory').check() is True
    assert file_path.check() is False


def server_process(directory):
    def run():
        os.chdir(directory)
        httpd = http.server.HTTPServer( ('', 6789), http.server.SimpleHTTPRequestHandler)
        httpd.serve_forever()
    
    p = Process(target=run)
    p.start()
    time.sleep(0.01)
    return p

def test_download_file(tmpdir):
    f = tmpdir.mkdir("www").join("file.txt")
    f.write('i am a file')
    dest = tmpdir.join('data/saved_filed.txt')
    p = server_process(tmpdir.strpath)
    assert dest.check() is False
    nycdb.dataset.download_file('http://127.0.0.1:6789/www/file.txt', dest.strpath)
    p.terminate()
    assert dest.check() is True
    assert tmpdir.join('data').check() is True
    assert dest.read() == 'i am a file'
    # This should return True and not attempt to download the file again:
    assert nycdb.dataset.download_file('http://localhost:6789/www/file.txt', dest.strpath)

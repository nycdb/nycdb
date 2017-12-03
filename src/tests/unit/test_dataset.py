import nycdb
import os
import time
import psycopg2

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
    

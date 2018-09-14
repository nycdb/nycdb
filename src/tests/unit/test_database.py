import nycdb
from unittest.mock import patch
from types import SimpleNamespace

# import pdb; pdb.set_trace()
ARGS = SimpleNamespace(user='postgres', password='password', host='127.0.0.1', database='postgres', port='7777', root_dir='/tmp/nycdb_test_data')

@patch('psycopg2.connect')
def test_init(psycopg2_connect_mock):
    db = nycdb.Database(ARGS, 'test_table')
    assert psycopg2_connect_mock.call_count == 1

    assert db.table_name == 'test_table'

    assert db.connection_params == {
        'user': 'postgres',
        'password': 'password',
        'host': '127.0.0.1',
        'database': 'postgres',
        'port': '7777'
    }

@patch('psycopg2.connect')
def test_password_file_contents(psycopg2_connect_mock):
    db = nycdb.Database(ARGS, 'test_table')
    assert db.password_file_contents() == "127.0.0.1:7777:postgres:postgres:password"

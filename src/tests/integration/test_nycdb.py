import psycopg2
import os
from types import SimpleNamespace
import nycdb

data_dir = os.path.join(os.path.dirname(__file__), 'data')

ARGS = SimpleNamespace(user='postgres', password='password', host='127.0.0.1', database='postgres', port='7777', root_dir=data_dir)


def connection():
    return psycopg2.connect(user=ARGS.user, password=ARGS.password, host=ARGS.host, database=ARGS.database, port=ARGS.port)


def drop_table(conn, table_name):
    with conn.cursor() as curs:
        curs.execute('DROP TABLE IF EXISTS {};'.format(table_name))
    conn.commit()

def row_count(conn, table_name):
    with conn.cursor() as curs:
        curs.execute('select count(*) from {}'.format(table_name))
        return curs.fetchone()[0]

def test_hpd_complaints():
    conn = connection()
    drop_table(conn, 'hpd_complaints')
    hpd_complaints = nycdb.Dataset('hpd_complaints', args=ARGS)
    hpd_complaints.db_import()
    assert row_count(conn, 'hpd_complaints') == 100
    conn.close()


def test_dob_complaints():
    conn = connection()
    drop_table(conn, 'dob_complaints')
    dob_complaints = nycdb.Dataset('dob_complaints', args=ARGS)
    dob_complaints.db_import()
    assert row_count(conn, 'dob_complaints') == 100
    conn.close()


def test_pluto16v2():
    conn = connection()
    drop_table(conn, 'pluto_16v2')
    pluto = nycdb.Dataset('pluto_16v2', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_16v2') == 500
    conn.close()

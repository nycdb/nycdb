import psycopg2
import psycopg2.extras
import os
from types import SimpleNamespace
from decimal import Decimal
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


def test_pluto_insert():
    conn = connection()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        #import pdb; pdb.set_trace()
        curs.execute("select * from pluto_16v2 WHERE bbl = '1008820003'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['address'] == '369 PARK AVENUE SOUTH'
        assert rec['lotarea'] == 8032
        assert round(rec['lng'], 5) == Decimal('-73.98434')
        assert round(rec['lat'], 5) == Decimal('40.74211')

    
def test_hpd_violations():
    conn = connection()
    drop_table(conn, 'hpd_violations')
    hpd_violations = nycdb.Dataset('hpd_violations', args=ARGS)
    hpd_violations.db_import()
    assert row_count(conn, 'hpd_violations') == 100
    conn.close()

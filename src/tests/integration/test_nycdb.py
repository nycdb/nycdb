import psycopg2
import os
from types import SimpleNamespace
import nycdb

data_dir = os.path.join(os.path.dirname(__file__), 'data')

ARGS = SimpleNamespace(user='postgres', password='password', host='127.0.0.1', database='postgres', port='7777', root_dir=data_dir)


def test_hpd_complaints():
    conn = psycopg2.connect(user=ARGS.user, password=ARGS.password, host=ARGS.host, database=ARGS.database, port=ARGS.port)
    with conn.cursor() as curs:
        curs.execute('DROP TABLE IF EXISTS hpd_complaints;')
    conn.commit()

    hpd_complaints = nycdb.Dataset('hpd_complaints', args=ARGS)

    hpd_complaints.db_import()

    with conn.cursor() as curs:
        curs.execute('select count(*) from hpd_complaints')
        count = curs.fetchone()
        assert count[0] == 100
    
    conn.close()

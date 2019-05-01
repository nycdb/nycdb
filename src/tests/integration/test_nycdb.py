import psycopg2
import psycopg2.extras
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from types import SimpleNamespace
from decimal import Decimal
import subprocess
import sys
import pytest

import nycdb

data_dir = os.path.join(os.path.dirname(__file__), 'data')

ARGS = SimpleNamespace(
    user=os.environ.get('NYCDB_TEST_POSTGRES_USER', 'nycdb'),
    password=os.environ.get('NYCDB_TEST_POSTGRES_PASSWORD', 'nycdb'),
    host=os.environ.get('NYCDB_TEST_POSTGRES_HOST', '127.0.0.1'),
    database=os.environ.get('NYCDB_TEST_POSTGRES_DB', 'nycdb_test'),
    port=os.environ.get('NYCDB_TEST_POSTGRES_PORT', '7777'),
    root_dir=data_dir
)

CONNECT_ARGS = dict(
    user=ARGS.user,
    password=ARGS.password,
    host=ARGS.host,
    database=ARGS.database,
    port=ARGS.port
)


def create_db(dbname):
    args = CONNECT_ARGS.copy()
    del args['database']
    conn = psycopg2.connect(**args)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as curs:
        curs.execute('CREATE DATABASE ' + dbname)
    conn.close()


@pytest.fixture(scope="session")
def db():
    """
    Attempt to connect to the database, retrying if necessary, and also
    creating the database if it doesn't already exist.
    """

    retries_left = 5

    while True:
        try:
            psycopg2.connect(**CONNECT_ARGS).close()
            return
        except psycopg2.OperationalError as e:
            if 'database "{}" does not exist'.format(ARGS.database) in str(e):
                create_db(ARGS.database)
                retries_left -= 1
            elif retries_left:
                # It's possible the database is still starting up.
                time.sleep(2)
                retries_left -= 1
            else:
                raise e


@pytest.fixture
def conn(db):
    with psycopg2.connect(**CONNECT_ARGS) as conn:
        yield conn


def drop_table(conn, table_name):
    with conn.cursor() as curs:
        curs.execute('DROP TABLE IF EXISTS {};'.format(table_name))
    conn.commit()


def row_count(conn, table_name):
    with conn:
        with conn.cursor() as curs:
            curs.execute('select count(*) from {}'.format(table_name))
            return curs.fetchone()[0]


def has_one_row(conn, query):
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            return bool(curs.fetchone())


def table_columns(conn, table_name):
    sql = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(
        table_name)
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            return [x[0] for x in curs.fetchall()]


def test_ecb_violations(conn):
    drop_table(conn, 'ecb_violations')
    ecb_violations = nycdb.Dataset('ecb_violations', args=ARGS)
    ecb_violations.db_import()
    assert row_count(conn, 'ecb_violations') == 5


def test_hpd_complaint_problems(conn):
    drop_table(conn, 'hpd_complaint_problems')
    drop_table(conn, 'hpd_complaints')
    hpd_complaints = nycdb.Dataset('hpd_complaints', args=ARGS)
    hpd_complaints.db_import()
    assert row_count(conn, 'hpd_complaint_problems') == 9


def test_hpd_complaints(conn):
    drop_table(conn, 'hpd_complaint_problems')
    drop_table(conn, 'hpd_complaints')
    hpd_complaints = nycdb.Dataset('hpd_complaints', args=ARGS)
    hpd_complaints.db_import()
    assert row_count(conn, 'hpd_complaints') == 100


def test_dob_complaints(conn):
    drop_table(conn, 'dob_complaints')
    dob_complaints = nycdb.Dataset('dob_complaints', args=ARGS)
    dob_complaints.db_import()
    assert row_count(conn, 'dob_complaints') == 100


def test_pluto15v1(conn):
    drop_table(conn, 'pluto_15v1')
    pluto = nycdb.Dataset('pluto_15v1', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_15v1') == 50


def test_pluto16v2(conn):
    drop_table(conn, 'pluto_16v2')
    pluto = nycdb.Dataset('pluto_16v2', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_16v2') == 500


def test_pluto_insert(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from pluto_16v2 WHERE bbl = '1008820003'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['address'] == '369 PARK AVENUE SOUTH'
        assert rec['lotarea'] == 8032
        assert round(rec['lng'], 12) == -73.984339547978
        assert round(rec['lat'], 12) == 40.742121844634


def test_pluto17v1(conn):
    drop_table(conn, 'pluto_17v1')
    pluto = nycdb.Dataset('pluto_17v1', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_17v1') == 500


def test_pluto18v1(conn):
    drop_table(conn, 'pluto_18v1')
    pluto = nycdb.Dataset('pluto_18v1', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_18v1') == 50


def test_pluto18v2(conn):
    drop_table(conn, 'pluto_18v2')
    pluto = nycdb.Dataset('pluto_18v2', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_18v2') == 10


def test_hpd_violations(conn):
    drop_table(conn, 'hpd_violations')
    hpd_violations = nycdb.Dataset('hpd_violations', args=ARGS)
    hpd_violations.db_import()
    assert row_count(conn, 'hpd_violations') == 100


def test_hpd_violations_index(conn):
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_bbl_idx') is NOT NULL")
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_violationid_idx') is NOT NULL")
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_currentstatusid_idx') is NOT NULL")


def test_hpd_registrations(conn):
    drop_table(conn, 'hpd_registrations')
    drop_table(conn, 'hpd_contacts')
    ds = nycdb.Dataset('hpd_registrations', args=ARGS)
    ds.db_import()
    assert row_count(conn, 'hpd_registrations') == 100
    assert row_count(conn, 'hpd_contacts') == 100


def test_hpd_registrations_derived_tables(conn):
    assert row_count(conn, 'hpd_corporate_owners') > 10
    assert row_count(conn, 'hpd_registrations_grouped_by_bbl') > 10
    assert row_count(conn, 'hpd_business_addresses') > 10
    assert row_count(conn, 'hpd_registrations_grouped_by_bbl_with_contacts') > 10


def test_hpd_registrations_rows(conn):
    assert has_one_row(conn, "select * from hpd_registrations where bbl = '1017510116'")


def test_dof_sales(conn):
    drop_table(conn, 'dof_sales')
    dof_sales = nycdb.Dataset('dof_sales', args=ARGS)
    dof_sales.db_import()
    assert row_count(conn, 'dof_sales') == 70
    assert has_one_row(conn, "select 1 where to_regclass('public.dof_sales_bbl_idx') is NOT NULL")


def test_dobjobs(conn):
    drop_table(conn, 'dobjobs')
    dobjobs = nycdb.Dataset('dobjobs', args=ARGS)
    dobjobs.db_import()
    assert row_count(conn, 'dobjobs') == 100
    columns = table_columns(conn, 'dobjobs')
    # test for columns add in add_columns.sql
    assert 'address' in columns
    assert 'ownername' in columns
    # full text columns shouldn't be inserted by default
    assert 'ownername_tsvector' not in columns
    dobjobs.index()
    columns = table_columns(conn, 'dobjobs')
    assert 'ownername_tsvector' in columns
    assert 'applicantname_tsvector' in columns


def test_dobjobs_work_types(conn):
    drop_table(conn, 'dobjobs')
    dobjobs = nycdb.Dataset('dobjobs', args=ARGS)
    dobjobs.db_import()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from dobjobs WHERE job = '{}'".format('310077591'))
        rec = curs.fetchone()
        assert rec['landmarked'] is False
        assert rec['loftboard'] is None
        assert rec['pcfiled'] is True
        assert rec['mechanical'] is True

def test_rentstab(conn):
    drop_table(conn, 'rentstab')
    rentstab = nycdb.Dataset('rentstab', args=ARGS)
    rentstab.db_import()
    assert row_count(conn, 'rentstab') == 100
    assert has_one_row(conn, "select 1 where to_regclass('public.rentstab_ucbbl_idx') is NOT NULL")


def test_rentstab_summary(conn):
    drop_table(conn, 'rentstab_summary')
    rentstab_summary = nycdb.Dataset('rentstab_summary', args=ARGS)
    rentstab_summary.db_import()
    assert row_count(conn, 'rentstab_summary') == 100


def test_acris(conn):
    drop_table(conn, 'real_property_legals')
    drop_table(conn, 'real_property_master')
    drop_table(conn, 'real_property_parties')
    drop_table(conn, 'real_property_references')
    drop_table(conn, 'real_property_remarks')
    drop_table(conn, 'personal_property_legals')
    drop_table(conn, 'personal_property_master')
    drop_table(conn, 'personal_property_parties')
    drop_table(conn, 'personal_property_references')
    drop_table(conn, 'personal_property_remarks')
    drop_table(conn, 'acris_country_codes')
    drop_table(conn, 'acris_document_control_codes')
    drop_table(conn, 'acris_property_type_codes')
    drop_table(conn, 'acris_ucc_collateral_codes')
    acris = nycdb.Dataset('acris', args=ARGS)
    acris.db_import()
    assert row_count(conn, 'real_property_legals') == 100
    assert row_count(conn, 'real_property_master') == 100
    assert row_count(conn, 'real_property_parties') == 100
    assert row_count(conn, 'real_property_references') == 100
    assert row_count(conn, 'real_property_remarks') == 10
    assert row_count(conn, 'personal_property_legals') == 100
    assert row_count(conn, 'personal_property_master') == 100
    assert row_count(conn, 'personal_property_parties') == 100
    assert row_count(conn, 'personal_property_references') == 10
    assert row_count(conn, 'personal_property_remarks') == 10
    assert row_count(conn, 'acris_country_codes') == 250
    assert row_count(conn, 'acris_document_control_codes') == 123
    assert row_count(conn, 'acris_property_type_codes') == 46
    assert row_count(conn, 'acris_ucc_collateral_codes') == 8
    assert has_one_row(conn, "select * from real_property_legals where bbl = '4131600009'")


def test_marshal_evictions(conn):
    drop_table(conn, 'marshal_evictions_17')
    drop_table(conn, 'marshal_evictions_18')
    evictions = nycdb.Dataset('marshal_evictions', args=ARGS)
    evictions.db_import()

    assert row_count(conn, 'marshal_evictions_17') == 10
    test_id = '60479/177111610280'
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from marshal_evictions_17 WHERE uniqueid = '{}'".format(test_id))
        rec = curs.fetchone()
        assert rec is not None
        assert rec['lat'] == Decimal('40.71081')

    assert row_count(conn, 'marshal_evictions_18') == 100


def test_oath_hearings(conn):
    drop_table(conn, 'oath_hearings')
    oath_hearings = nycdb.Dataset('oath_hearings', args=ARGS)
    oath_hearings.db_import()
    assert row_count(conn, 'oath_hearings') == 100
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from oath_hearings WHERE bbl = '{}'".format('1020260001'))
        rec = curs.fetchone()
        assert rec is not None
        assert rec['totalviolationamount'] == Decimal('40000.00')


def test_dob_violations(conn):
    drop_table(conn, 'dob_violations')
    dob_violations = nycdb.Dataset('dob_violations', args=ARGS)
    dob_violations.db_import()
    assert row_count(conn, 'dob_violations') == 100
    # 3028850001
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from dob_violations WHERE bbl = '{}'".format('3028850001'))
        rec = curs.fetchone()
        assert rec is not None
        assert rec['violationtypecode'] == 'LL6291'


def test_j51_exemptions(conn):
    drop_table(conn, 'j51_exemptions')
    j51_exemptions = nycdb.Dataset('j51_exemptions', args=ARGS)
    j51_exemptions.db_import()
    assert row_count(conn, 'j51_exemptions') == 100
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute("select * from j51_exemptions WHERE bbl = '1000151001'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['taxyear'] == 2001


def run_cli(args, input):
    full_args = [
        sys.executable, "-m", "nycdb.cli",
        "--user", ARGS.user,
        "--password", ARGS.password,
        "--host", ARGS.host,
        "--database", ARGS.database,
        "--port", ARGS.port,
        "--root-dir", ARGS.root_dir,
        *args
    ]

    print("Running '{}'...".format(' '.join(full_args)))

    proc = subprocess.Popen(
        full_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    try:
        outs, errs = proc.communicate(input, timeout=10)
    except subprocess.TimeoutExpired as e:
        proc.kill()
        outs, errs = proc.communicate()

    if proc.returncode != 0:
        sys.stdout.write(outs)
        sys.stderr.write(errs)
        raise Exception('Subprocess failed, see stdout/stderr')

    return outs, errs


def test_dbshell(db):
    outs, errs = run_cli(["--dbshell"], input="\\copyright")
    assert 'PostgreSQL' in outs

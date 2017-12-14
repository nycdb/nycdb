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
    sql ="SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(table_name)
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            return [ x[0] for x in curs.fetchall() ]

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


def test_hpd_violations_index():
    conn = connection()
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_bbl_idx') is NOT NULL")
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_violationid_idx') is NOT NULL")
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_violations_currentstatusid_idx') is NOT NULL")
    conn.close()


def test_hpd_registrations():
    conn = connection()
    drop_table(conn, 'hpd_registrations')
    drop_table(conn, 'hpd_contacts')
    ds = nycdb.Dataset('hpd_registrations', args=ARGS)
    ds.db_import()
    assert row_count(conn, 'hpd_registrations') == 100
    assert row_count(conn, 'hpd_contacts') == 100
    conn.close()

def test_hpd_registrations_derived_tables():
    conn = connection()
    assert row_count(conn, 'hpd_corporate_owners') > 10
    assert row_count(conn, 'hpd_registrations_grouped_by_bbl') > 10
    assert row_count(conn, 'hpd_business_addresses') > 10
    assert row_count(conn, 'hpd_registrations_grouped_by_bbl_with_contacts') > 10
    conn.close()

def test_hpd_registrations_rows():
    conn = connection()
    assert has_one_row(conn, "select * from hpd_registrations where bbl = '1017510116'")
    conn.close()

def test_dof_sales():
    conn = connection()
    drop_table(conn, 'dof_sales')
    dof_sales = nycdb.Dataset('dof_sales', args=ARGS)
    dof_sales.db_import()
    assert row_count(conn, 'dof_sales') == 140
    assert has_one_row(conn, "select 1 where to_regclass('public.dof_sales_bbl_idx') is NOT NULL")
    conn.close()
    
def test_dobjobs():
    conn = connection()
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
    conn.close()

def test_rentstab():
    conn = connection()
    drop_table(conn, 'rentstab')
    rentstab = nycdb.Dataset('rentstab', args=ARGS)
    rentstab.db_import()
    assert row_count(conn, 'rentstab') == 100
    assert has_one_row(conn, "select 1 where to_regclass('public.rentstab_ucbbl_idx') is NOT NULL")
    conn.close()

def test_acris():
    conn = connection()
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
    conn.close()

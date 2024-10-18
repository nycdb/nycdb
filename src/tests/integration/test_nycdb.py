import psycopg
from psycopg.rows import dict_row
import time
import os
from types import SimpleNamespace
from decimal import Decimal
import subprocess
import sys
import pytest

import nycdb

data_dir = os.path.join(os.path.dirname(__file__), "data")

ARGS = SimpleNamespace(
    user=os.environ.get("NYCDB_TEST_POSTGRES_USER", "nycdb"),
    password=os.environ.get("NYCDB_TEST_POSTGRES_PASSWORD", "nycdb"),
    host=os.environ.get("NYCDB_TEST_POSTGRES_HOST", "127.0.0.1"),
    database=os.environ.get("NYCDB_TEST_POSTGRES_DB", "nycdb_test"),
    port=os.environ.get("NYCDB_TEST_POSTGRES_PORT", "7777"),
    root_dir=data_dir,
    hide_progress=False,
)

CONNINFO = f"host={ARGS.host} port={ARGS.port} dbname={ARGS.database} user={ARGS.user} password={ARGS.password}"


def create_db(dbname):
    conn = psycopg.connect(CONNINFO, autocommit=True)
    with conn.cursor() as curs:
        curs.execute("CREATE DATABASE " + dbname)
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
            psycopg.connect(CONNINFO).close()
            return
        except psycopg.OperationalError as e:
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
    with psycopg.connect(CONNINFO) as conn:
        yield conn


def drop_table(conn, table_name):
    with conn.cursor() as curs:
        curs.execute("DROP TABLE IF EXISTS {};".format(table_name))
    conn.commit()


def setup_postgis(conn):
    with conn.cursor() as curs:
        curs.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    conn.commit()


def get_srid(conn, table_name, column_name):
    with conn.cursor() as curs:
        curs.execute(f"SELECT ST_SRID({column_name}) from {table_name}")
        return curs.fetchone()[0]


def row_count(conn, table_name):
    with conn.cursor() as curs:
        curs.execute("select count(*) from {}".format(table_name))
        return curs.fetchone()[0]


def fetch_one_row(conn, query):
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(query)
        return curs.fetchone()


def has_one_row(*args):
    return bool(fetch_one_row(*args))


def has_index(conn, index_name):
    return has_one_row(conn, f"select 1 where to_regclass('public.{index_name}') is NOT NULL")


def table_columns(conn, table_name):
    sql = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(
        table_name
    )
    with conn.cursor() as curs:
        curs.execute(sql)
        return [x[0] for x in curs.fetchall()]


def test_ecb_violations(conn):
    drop_table(conn, "ecb_violations")
    ecb_violations = nycdb.Dataset("ecb_violations", args=ARGS)
    ecb_violations.db_import()
    assert row_count(conn, "ecb_violations") == 5


def test_hpd_complaints(conn):
    drop_table(conn, "hpd_complaints_and_problems")
    hpd_complaints = nycdb.Dataset("hpd_complaints", args=ARGS)
    hpd_complaints.db_import()
    assert row_count(conn, "hpd_complaints_and_problems") == 10


def test_dof_exemptions(conn):
    drop_table(conn, "dof_exemptions")
    drop_table(conn, "dof_exemption_classification_codes")
    dof_exemptions = nycdb.Dataset("dof_exemptions", args=ARGS)
    dof_exemptions.db_import()
    assert row_count(conn, "dof_exemptions") == 10


def test_dof_exemption_classification_codes(conn):
    drop_table(conn, "dof_exemptions")
    drop_table(conn, "dof_exemption_classification_codes")
    dof_exemptions = nycdb.Dataset("dof_exemptions", args=ARGS)
    dof_exemptions.db_import()
    assert row_count(conn, "dof_exemption_classification_codes") == 10


def test_dob_complaints(conn):
    drop_table(conn, "dob_complaints")
    dob_complaints = nycdb.Dataset("dob_complaints", args=ARGS)
    dob_complaints.db_import()
    assert row_count(conn, "dob_complaints") == 100


def test_pluto10v1(conn):
    drop_table(conn, "pluto_10v1")
    pluto = nycdb.Dataset("pluto_10v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_10v1") == 20


def test_pluto15v1(conn):
    drop_table(conn, "pluto_15v1")
    pluto = nycdb.Dataset("pluto_15v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_15v1") == 50


def test_pluto16v2(conn):
    drop_table(conn, "pluto_16v2")
    pluto = nycdb.Dataset("pluto_16v2", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_16v2") == 500


def test_pluto_insert(conn):
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from pluto_16v2 WHERE bbl = '1008820003'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["address"] == "369 PARK AVENUE SOUTH"
        assert rec["lotarea"] == 8032


def test_pluto17v1(conn):
    drop_table(conn, "pluto_17v1")
    pluto = nycdb.Dataset("pluto_17v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_17v1") == 500


def test_pluto18v1(conn):
    drop_table(conn, "pluto_18v1")
    pluto = nycdb.Dataset("pluto_18v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_18v1") == 50


def test_pluto18v2(conn):
    drop_table(conn, "pluto_18v2")
    pluto = nycdb.Dataset("pluto_18v2", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_18v2") == 10


def test_pluto19v1(conn):
    drop_table(conn, "pluto_19v1")
    pluto = nycdb.Dataset("pluto_19v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_19v1") == 10


def test_pluto19v2(conn):
    drop_table(conn, "pluto_19v2")
    pluto = nycdb.Dataset("pluto_19v2", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_19v2") == 10


def test_pluto20v8(conn):
    drop_table(conn, "pluto_20v8")
    pluto = nycdb.Dataset("pluto_20v8", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_20v8") == 10


def test_pluto21v3(conn):
    drop_table(conn, "pluto_21v3")
    pluto = nycdb.Dataset("pluto_21v3", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_21v3") == 5


def test_pluto22v1(conn):
    drop_table(conn, "pluto_22v1")
    pluto = nycdb.Dataset("pluto_22v1", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_22v1") == 5


def test_pluto23v1(conn):
    drop_table(conn, 'pluto_23v1')
    pluto = nycdb.Dataset('pluto_23v1', args=ARGS)
    pluto.db_import()
    assert row_count(conn, 'pluto_23v1') == 5


def test_pluto_24v2(conn):
    drop_table(conn, 'pluto_24v2')
    dataset = nycdb.Dataset('pluto_24v2', args=ARGS)
    dataset.db_import()
    assert row_count(conn, 'pluto_24v2') == 5


def test_pluto_latest(conn):
    drop_table(conn, "pluto_latest")
    pluto = nycdb.Dataset("pluto_latest", args=ARGS)
    pluto.db_import()
    assert row_count(conn, "pluto_latest") == 5


def test_pluto_sql_columns(conn):
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from pluto_latest WHERE landuse = 1")
        rec = curs.fetchone()
        assert rec["landusedesc"] == "One & Two Family Buildings"


def test_hpd_violations(conn):
    drop_table(conn, "hpd_violations")
    hpd_violations = nycdb.Dataset("hpd_violations", args=ARGS)
    hpd_violations.db_import()
    assert row_count(conn, "hpd_violations") == 100


def test_hpd_charges(conn):
    dataset = nycdb.Dataset('hpd_charges', args=ARGS)
    dataset.drop()
    dataset.db_import()
    for s in dataset.schemas:
        assert row_count(conn, s['table_name']) == 5


def test_hpd_violations_index(conn):
    assert has_one_row(
        conn, "select 1 where to_regclass('public.hpd_violations_bbl_idx') is NOT NULL"
    )
    assert has_one_row(
        conn,
        "select 1 where to_regclass('public.hpd_violations_violationid_idx') is NOT NULL",
    )
    assert has_one_row(
        conn,
        "select 1 where to_regclass('public.hpd_violations_currentstatusid_idx') is NOT NULL",
    )


def test_hpd_registrations(conn):
    drop_table(conn, "hpd_registrations")
    drop_table(conn, "hpd_contacts")
    ds = nycdb.Dataset("hpd_registrations", args=ARGS)
    ds.db_import()
    assert row_count(conn, "hpd_registrations") == 100
    assert row_count(conn, "hpd_contacts") == 100


def test_hpd_litigations(conn):
    drop_table(conn, "hpd_litigations")
    hpd_litigations = nycdb.Dataset("hpd_litigations", args=ARGS)
    hpd_litigations.db_import()
    assert row_count(conn, "hpd_litigations") == 100


def test_hpd_registrations_derived_tables(conn):
    assert row_count(conn, "hpd_corporate_owners") > 10
    assert row_count(conn, "hpd_registrations_grouped_by_bbl") > 10
    assert row_count(conn, "hpd_business_addresses") > 10
    assert row_count(conn, "hpd_registrations_grouped_by_bbl_with_contacts") > 10


def test_hpd_registrations_rows(conn):
    assert has_one_row(conn, "select * from hpd_registrations where bbl = '1017510116'")


def test_dof_sales(conn):
    drop_table(conn, "dof_sales")
    dof_sales = nycdb.Dataset("dof_sales", args=ARGS)
    dof_sales.db_import()
    assert row_count(conn, "dof_sales") == 10
    assert has_one_row(
        conn, "select 1 where to_regclass('public.dof_sales_bbl_idx') is NOT NULL"
    )


def test_dobjobs(conn):
    drop_table(conn, "dobjobs")
    drop_table(conn, "dob_now_jobs")
    dobjobs = nycdb.Dataset("dobjobs", args=ARGS)
    dobjobs.db_import()
    assert row_count(conn, "dobjobs") == 100
    columns = table_columns(conn, "dobjobs")
    # test for columns add in add_columns.sql
    assert "address" in columns
    assert "ownername" in columns
    # full text columns shouldn't be inserted by default
    assert "ownername_tsvector" not in columns

    # without this commit, the database connection seems to deadlock
    # oddly, setting autocommit on the connection doesn't fix it either
    conn.commit()

    dobjobs.index()
    columns = table_columns(conn, "dobjobs")
    assert "ownername_tsvector" in columns
    assert "applicantname_tsvector" in columns


def test_dobjobs_work_types(conn):
    drop_table(conn, "dobjobs")
    drop_table(conn, "dob_now_jobs")
    dobjobs = nycdb.Dataset("dobjobs", args=ARGS)
    dobjobs.db_import()

    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dobjobs WHERE job = '{}'".format("310077591"))
        rec = curs.fetchone()
        assert rec["landmarked"] is False
        assert rec["loftboard"] is None
        assert rec["pcfiled"] is True
        assert rec["mechanical"] is True


def test_dob_now_jobs(conn):
    drop_table(conn, "dobjobs")
    drop_table(conn, "dob_now_jobs")
    dob_now_jobs = nycdb.Dataset("dobjobs", args=ARGS)
    dob_now_jobs.db_import()
    assert row_count(conn, "dob_now_jobs") == 5
    assert has_one_row(
        conn, "select 1 where to_regclass('public.dob_now_jobs_bbl') is NOT NULL"
    )


def test_rentstab(conn):
    drop_table(conn, "rentstab")
    rentstab = nycdb.Dataset("rentstab", args=ARGS)
    rentstab.db_import()
    assert row_count(conn, "rentstab") == 100
    assert has_one_row(
        conn, "select 1 where to_regclass('public.rentstab_ucbbl_idx') is NOT NULL"
    )


def test_rentstab_summary(conn):
    drop_table(conn, "rentstab_summary")
    rentstab_summary = nycdb.Dataset("rentstab_summary", args=ARGS)
    rentstab_summary.db_import()
    assert row_count(conn, "rentstab_summary") == 100


def test_rentstab_v2(conn):
    drop_table(conn, "rentstab_v2")
    rentstab_v2 = nycdb.Dataset("rentstab_v2", args=ARGS)
    rentstab_v2.db_import()
    assert row_count(conn, "rentstab_v2") == 100


def test_acris(conn):
    drop_table(conn, "real_property_legals")
    drop_table(conn, "real_property_master")
    drop_table(conn, "real_property_parties")
    drop_table(conn, "real_property_references")
    drop_table(conn, "real_property_remarks")
    drop_table(conn, "personal_property_legals")
    drop_table(conn, "personal_property_master")
    drop_table(conn, "personal_property_parties")
    drop_table(conn, "personal_property_references")
    drop_table(conn, "personal_property_remarks")
    drop_table(conn, "acris_country_codes")
    drop_table(conn, "acris_document_control_codes")
    drop_table(conn, "acris_property_type_codes")
    drop_table(conn, "acris_ucc_collateral_codes")
    acris = nycdb.Dataset("acris", args=ARGS)
    acris.db_import()
    assert row_count(conn, "real_property_legals") == 100
    assert row_count(conn, "real_property_master") == 100
    assert row_count(conn, "real_property_parties") == 100
    assert row_count(conn, "real_property_references") == 100
    assert row_count(conn, "real_property_remarks") == 10
    assert row_count(conn, "personal_property_legals") == 100
    assert row_count(conn, "personal_property_master") == 100
    assert row_count(conn, "personal_property_parties") == 100
    assert row_count(conn, "personal_property_references") == 10
    assert row_count(conn, "personal_property_remarks") == 10
    assert row_count(conn, "acris_country_codes") == 250
    assert row_count(conn, "acris_document_control_codes") == 123
    assert row_count(conn, "acris_property_type_codes") == 46
    assert row_count(conn, "acris_ucc_collateral_codes") == 8
    assert has_one_row(
        conn, "select * from real_property_legals where bbl = '4131600009'"
    )


def test_marshal_evictions(conn):
    drop_table(conn, "marshal_evictions_17")
    drop_table(conn, "marshal_evictions_18")
    drop_table(conn, "marshal_evictions_19")
    drop_table(conn, "marshal_evictions_all")
    evictions = nycdb.Dataset("marshal_evictions", args=ARGS)
    evictions.db_import()

    assert row_count(conn, "marshal_evictions_17") == 10
    test_id = "60479/177111610280"
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            "select * from marshal_evictions_17 WHERE uniqueid = '{}'".format(test_id)
        )
        rec = curs.fetchone()
        assert rec is not None
        assert rec["lat"] == Decimal("40.71081")

    assert row_count(conn, "marshal_evictions_18") == 100
    assert row_count(conn, "marshal_evictions_19") == 100
    assert row_count(conn, "marshal_evictions_all") == 100


def test_oath_hearings(conn):
    drop_table(conn, "oath_hearings")
    oath_hearings = nycdb.Dataset("oath_hearings", args=ARGS)
    oath_hearings.db_import()
    assert row_count(conn, "oath_hearings") == 100
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            "select * from oath_hearings WHERE bbl = '{}'".format("1020260001")
        )
        rec = curs.fetchone()
        assert rec is not None
        assert rec["totalviolationamount"] == Decimal("40000.00")


def test_dob_violations(conn):
    drop_table(conn, "dob_violations")
    dob_violations = nycdb.Dataset("dob_violations", args=ARGS)
    dob_violations.db_import()
    assert row_count(conn, "dob_violations") == 100
    # 3028850001
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            "select * from dob_violations WHERE bbl = '{}'".format("3028850001")
        )
        rec = curs.fetchone()
        assert rec is not None
        assert rec["violationtypecode"] == "LL6291"


def test_pad(conn):
    drop_table(conn, "pad_adr")
    pad = nycdb.Dataset("pad", args=ARGS)
    pad.db_import()
    assert row_count(conn, "pad_adr") == 100
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from pad_adr WHERE bin = '1086410'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["bbl"] == "1000010010"


def test_j51_exemptions(conn):
    drop_table(conn, "j51_exemptions")
    j51_exemptions = nycdb.Dataset("j51_exemptions", args=ARGS)
    j51_exemptions.db_import()
    assert row_count(conn, "j51_exemptions") == 100
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from j51_exemptions WHERE bbl = '1000151001'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["taxyear"] == 2001


def test_hpd_vacateorders(conn):
    drop_table(conn, "hpd_vacateorders")
    dataset = nycdb.Dataset("hpd_vacateorders", args=ARGS)
    dataset.db_import()
    assert row_count(conn, "hpd_vacateorders") == 100
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_vacateorders WHERE vacateordernumber = 100282")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["bbl"] == "3013480010"


def test_mci_applications(conn):
    drop_table(conn, "mci_applications")
    mci_applications = nycdb.Dataset("mci_applications", args=ARGS)
    mci_applications.db_import()
    assert row_count(conn, "mci_applications") == 100
    assert has_one_row(
        conn,
        "select 1 where to_regclass('public.mci_applications_bbl_idx') is NOT NULL",
    )

    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from mci_applications WHERE bin = '2012083'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["bbl"] == "2030710039"
        assert rec["filingdate"].strftime("%Y-%m-%d") == "2018-11-09"


def test_oca(conn):
    drop_table(conn, "oca_index")
    drop_table(conn, "oca_causes")
    drop_table(conn, "oca_addresses")
    drop_table(conn, "oca_parties")
    drop_table(conn, "oca_events")
    drop_table(conn, "oca_appearances")
    drop_table(conn, "oca_appearance_outcomes")
    drop_table(conn, "oca_motions")
    drop_table(conn, "oca_decisions")
    drop_table(conn, "oca_judgments")
    drop_table(conn, "oca_warrants")
    drop_table(conn, "oca_metadata")
    oca = nycdb.Dataset("oca", args=ARGS)
    oca.db_import()
    assert row_count(conn, "oca_index") == 100
    assert row_count(conn, "oca_causes") == 100
    assert row_count(conn, "oca_addresses") == 100
    assert row_count(conn, "oca_parties") == 100
    assert row_count(conn, "oca_events") == 100
    assert row_count(conn, "oca_appearances") == 100
    assert row_count(conn, "oca_appearance_outcomes") == 100
    assert row_count(conn, "oca_motions") == 100
    assert row_count(conn, "oca_decisions") == 100
    assert row_count(conn, "oca_judgments") == 100
    assert row_count(conn, "oca_warrants") == 100
    assert row_count(conn, "oca_metadata") == 100
    test_id = "000146FB4347DEDD75BD9817F6FA786E6B978ACA16FA54CAEDD5D48B16DD53E5"
    assert has_one_row(
        conn, f"select * from oca_index where indexnumberid = '{test_id}'"
    )
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            "select * from oca_index WHERE indexnumberid = '{}'".format(test_id)
        )
        rec = curs.fetchone()
        assert rec is not None
        assert rec["court"] == "Kings County Civil Court"
        assert rec["fileddate"].strftime("%Y-%m-%d") == "2016-02-04"
        assert rec["specialtydesignationtypes"] == ["Specialty (HHP) Zipcodes"]
        assert rec["primaryclaimtotal"] == Decimal("2740.46")
    # make sure datatimes are working
    test_id = "00000131D2D43B62D4764607D1AB017FC536618A72F3795716341A8DD100CBEF"
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            "select * from oca_appearances WHERE indexnumberid = '{}'".format(test_id)
        )
        rec = curs.fetchone()
        assert rec is not None
        assert (
            rec["appearancedatetime"].strftime("%Y-%m-%d %I:%M:%S")
            == "2016-05-11 09:30:00"
        )


def test_dof_annual_sales(conn):
    drop_table(conn, "dof_annual_sales")
    dof_annual_sales = nycdb.Dataset("dof_annual_sales", args=ARGS)
    dof_annual_sales.files = [
        nycdb.file.File(
            {
                "dest": "dof_annual_sales_2020_manhattan.xlsx",
                "url": "https://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/annualized-sales/2020/2020_manhattan.xlsx",
            },
            root_dir=data_dir,
        ),
        nycdb.file.File(
            {
                "dest": "dof_annual_sales_2015_manhattan.xls",
                "url": "https://www1.nyc.gov/assets/finance/downloads/pdf/rolling_sales/annualized-sales/2015/2015_manhattan.xls",
            },
            root_dir=data_dir,
        ),
    ]

    dof_annual_sales.db_import()
    assert row_count(conn, "dof_annual_sales") == 47


def test_dof_421a(conn):
    drop_table(conn, "dof_421a")
    dof_421a = nycdb.Dataset("dof_421a", args=ARGS)
    dof_421a.files = [
        nycdb.file.File(
            {"dest": "421a_2021_brooklyn.xlsx", "url": "https://example.com"},
            root_dir=data_dir,
        )
    ]
    dof_421a.db_import()
    assert row_count(conn, "dof_421a") == 45
    assert fetch_one_row(conn, "SELECT * FROM dof_421a LIMIT 1")["fiscalyear"] == "2021"


def test_speculation_watch_list(conn):
    drop_table(conn, "speculation_watch_list")
    speculation_watch_list = nycdb.Dataset("speculation_watch_list", args=ARGS)
    speculation_watch_list.db_import()
    assert row_count(conn, "speculation_watch_list") == 5


def test_hpd_affordable_production(conn):
    drop_table(conn, "hpd_affordable_building")
    drop_table(conn, "hpd_affordable_project")
    hpd_affordable_production = nycdb.Dataset("hpd_affordable_production", args=ARGS)
    hpd_affordable_production.db_import()
    assert row_count(conn, "hpd_affordable_building") == 5
    assert row_count(conn, "hpd_affordable_project") == 5


def test_hpd_conh(conn):
    drop_table(conn, "hpd_conh")
    hpd_conh = nycdb.Dataset("hpd_conh", args=ARGS)
    hpd_conh.db_import()
    assert row_count(conn, "hpd_conh") == 5
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_conh_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_conh WHERE bbl = '1014570003'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["nta"] == "MN0801"


def run_cli(args, input):
    full_args = [
        sys.executable,
        "-m",
        "nycdb.cli",
        "--user",
        ARGS.user,
        "--password",
        ARGS.password,
        "--host",
        ARGS.host,
        "--database",
        ARGS.database,
        "--port",
        ARGS.port,
        "--root-dir",
        ARGS.root_dir,
        *args,
    ]

    print("Running '{}'...".format(" ".join(full_args)))

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
        raise Exception("Subprocess failed, see stdout/stderr")

    return outs, errs


def test_dbshell(db):
    outs, errs = run_cli(["--dbshell"], input="\\copyright")
    assert "PostgreSQL" in outs


def test_dcp_housingdb(conn):
    drop_table(conn, "dcp_housingdb")
    dataset = nycdb.Dataset("dcp_housingdb", args=ARGS)
    dataset.db_import()
    assert row_count(conn, "dcp_housingdb") > 0
    assert has_one_row(
        conn, "select 1 where to_regclass('public.dcp_housingdb_bbl_idx') is NOT NULL"
    )

    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dcp_housingdb WHERE jobnumber = '102138820'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["latitude"] == Decimal("40.796734999999998")


def test_dob_vacate_orders(conn):
    drop_table(conn, "dob_vacate_orders")
    dataset = nycdb.Dataset("dob_vacate_orders", args=ARGS)
    dataset.db_import()
    assert row_count(conn, "dob_vacate_orders") > 0
    assert has_one_row(
        conn,
        "select 1 where to_regclass('public.dob_vacate_orders_bbl_idx') is NOT NULL",
    )

    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dob_vacate_orders WHERE bbl = '4029700038'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["lastdispositiondate"].strftime("%Y-%m-%d") == "2012-01-03"


def test_dof_tax_lien_sale_list(conn):
    drop_table(conn, "dof_tax_lien_sale_list")
    dataset = nycdb.Dataset("dof_tax_lien_sale_list", args=ARGS)
    dataset.db_import()
    assert row_count(conn, "dof_tax_lien_sale_list") > 0
    assert has_one_row(
        conn,
        "select 1 where to_regclass('public.dof_tax_lien_sale_list_bbl_idx') is NOT NULL",
    )
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dof_tax_lien_sale_list WHERE bbl = '1000160003'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["reportdate"].strftime("%Y-%m-%d") == "2019-04-01"


def test_dob_certificate_occupancy(conn):
    dob_certificate_occupancy = nycdb.Dataset('dob_certificate_occupancy', args=ARGS)
    dob_certificate_occupancy.drop()
    dob_certificate_occupancy.db_import()
    assert row_count(conn, 'dob_certificate_occupancy') == 5
    assert row_count(conn, 'dob_foil_certificate_occupancy') == 5
    assert has_one_row(conn,"select 1 where to_regclass('public.dob_certificate_occupancy_bbl_idx') is NOT NULL")
    assert has_one_row(conn,"select 1 where to_regclass('public.dob_foil_certificate_occupancy_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dob_certificate_occupancy WHERE bbl = '2051410035'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["jobnumber"] == "220466350"

        curs.execute("select * from dob_foil_certificate_occupancy WHERE bbl = '1012440025'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec["jobnumber"] == "100031528"



def test_dob_safety_violations(conn):
    drop_table(conn, 'dob_safety_violations')
    dob_safety_violations = nycdb.Dataset('dob_safety_violations', args=ARGS)
    dob_safety_violations.db_import()
    assert row_count(conn, 'dob_safety_violations') == 9


def test_shapefile_in_alt_schema_works(conn):
    setup_postgis(conn)
    boundaries = nycdb.Dataset('boundaries', args=ARGS)
    boundaries.setup_db()
    default_search_path = boundaries.db.execute_and_fetchone("SHOW search_path")
    boundaries.db.sql("CREATE SCHEMA IF NOT EXISTS temp; SET search_path TO temp, public")
    boundaries.db_import()
    query = "SELECT table_schema FROM information_schema.columns WHERE table_name='nyad'"
    assert boundaries.db.execute_and_fetchone(query) == "temp"
    boundaries.db.sql(f'DROP SCHEMA temp CASCADE; SET search_path TO {default_search_path};')


def test_boundaries(conn):
    setup_postgis(conn)
    boundaries = nycdb.Dataset('boundaries', args=ARGS)
    boundaries.drop()
    boundaries.db_import()
    assert row_count(conn, 'nyad') == 5
    assert row_count(conn, 'nycc') == 5
    assert get_srid(conn, 'nycc', 'geom') == 2263
    assert has_one_row(
        conn, "select 1 where to_regclass('public.nyad_geom_idx') is NOT NULL"
    )


def test_dhs_daily_shelter_count(conn):
    drop_table(conn, 'dhs_daily_shelter_count')
    ecb_violations = nycdb.Dataset('dhs_daily_shelter_count', args=ARGS)
    ecb_violations.db_import()
    assert row_count(conn, 'dhs_daily_shelter_count') == 5


def test_dohmh_rodent_inspections(conn):
    drop_table(conn, 'dohmh_rodent_inspections')
    dataset = nycdb.Dataset('dohmh_rodent_inspections', args=ARGS)
    dataset.db_import()
    assert row_count(conn, 'dohmh_rodent_inspections') == 5
    assert has_one_row(conn, "select 1 where to_regclass('public.dohmh_rodent_inspections_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from dohmh_rodent_inspections WHERE bbl = '1000520021'")
        rec = curs.fetchone()
        assert rec is not None
        print(rec)
        assert rec['inspectiondate'].strftime("%Y-%m-%d") == '2021-03-26'
        assert rec['approveddate'].strftime("%Y-%m-%d") == '2021-03-29'


def test_hpd_aep(conn):
    dataset = nycdb.Dataset('hpd_aep', args=ARGS)
    dataset.drop()
    dataset.db_import()
    assert row_count(conn, 'hpd_aep') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_aep_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_aep WHERE bbl = '2031560155'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['buildingid'] == 107767


def test_hpd_underlying_conditions(conn):
    dataset = nycdb.Dataset('hpd_underlying_conditions', args=ARGS)
    dataset.drop()
    dataset.db_import()
    assert row_count(conn, 'hpd_underlying_conditions') == 5
    assert has_index(conn, 'hpd_underlying_conditions_bbl_idx')
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_underlying_conditions WHERE bbl = '2046280001'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['currentstatus'] == 'Discharged'


def test_nycha_bbls(conn):
    dataset = nycdb.Dataset('nycha_bbls', args=ARGS)
    dataset.drop()
    dataset.db_import()

    assert row_count(conn, 'nycha_bbls_24') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.nycha_bbls_24_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from nycha_bbls_24 WHERE bbl = '2023240001'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['development'] == 'PATTERSON'


def test_hpd_ll44(conn):
    dataset = nycdb.Dataset('hpd_ll44', args=ARGS)
    dataset.drop()
    dataset.db_import()
    
    assert row_count(conn, 'hpd_ll44_buildings') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_ll44_buildings_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_ll44_buildings WHERE buildingid = 987329")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['projectid'] == 44218
        assert rec['bbl'] == '1017900046'
        assert rec['boroid'] == 1

    assert row_count(conn, 'hpd_ll44_projects') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_ll44_projects_projectid_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_ll44_projects WHERE projectid = 44218")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['programgroup'] == 'Multifamily Finance Program'

    assert row_count(conn, 'hpd_ll44_tax_incentive') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.hpd_ll44_tax_incentive_projectid_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from hpd_ll44_tax_incentive WHERE projectid = 44218")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['taxincentivename'] == 'Article XI'


def test_fc_shd(conn):
    drop_table(conn, 'fc_shd')
    dataset = nycdb.Dataset('fc_shd', args=ARGS)
    dataset.db_import()
    assert row_count(conn, 'fc_shd_building') > 0
    assert has_one_row(conn, "select 1 where to_regclass('public.fc_shd_building_bbl_idx') is NOT NULL")
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute("select * from fc_shd_building WHERE bbl = '1000160015'")
        rec = curs.fetchone()
        assert rec is not None
        assert rec['proglihtc4'] == True
        assert rec['startlihtc4'].strftime("%Y-%m-%d") == '2000-01-01'
